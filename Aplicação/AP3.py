from machine import Pin, I2C, PWM
import utime
from MPU6050 import init_mpu6050, get_mpu6050_data
from encoder import EncoderSimulator

# Definição dos pinos I2C
I2C_SDA_PIN = 0  # Pino SDA para comunicação I2C
I2C_SCL_PIN = 1  # Pino SCL para comunicação I2C

# Inicializa a comunicação I2C com os pinos definidos e frequência de 400kHz
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)

# Inicializa o sensor MPU6050
init_mpu6050(i2c)

# Função para calibrar o sensor
def calibrate_sensor(i2c, samples=100):
    accel_offset = {'x': 0, 'y': 0, 'z': 0}
    gyro_offset = {'x': 0, 'y': 0, 'z': 0}
    
    for _ in range(samples):
        data = get_mpu6050_data(i2c)
        accel_offset['x'] += data['accel']['x']
        accel_offset['y'] += data['accel']['y']
        accel_offset['z'] += data['accel']['z']
        gyro_offset['x'] += data['gyro']['x']
        gyro_offset['y'] += data['gyro']['y']
        gyro_offset['z'] += data['gyro']['z']
        utime.sleep(0.01)  # Espera um pouco entre as leituras

    # Calcula a média
    accel_offset = {k: v / samples for k, v in accel_offset.items()}
    gyro_offset = {k: v / samples for k, v in gyro_offset.items()}
    
    return accel_offset, gyro_offset

# Calibra o sensor e obtém os desvios
accel_offset, gyro_offset = calibrate_sensor(i2c)

# Variáveis para armazenar as leituras anteriores
previous_accel = {'x': 0, 'y': 0, 'z': 0}
previous_gyro = {'x': 0, 'y': 0, 'z': 0}

# Limite para detectar mudanças bruscas
accel_threshold = 0.5  # Limite para aceleração em g
gyro_threshold = 10.0  # Limite para giroscópio em °/s

# Funções para controle do movimento
motor_esquerda_frente = PWM(Pin(8), freq=1000)
motor_esquerda_tras = PWM(Pin(7), freq=1000)
motor_direita_frente = PWM(Pin(9), freq=1000)
motor_direita_tras = PWM(Pin(10), freq=1000)

def parar():
    motor_esquerda_frente.duty_u16(0)
    motor_esquerda_tras.duty_u16(0)
    motor_direita_frente.duty_u16(0)
    motor_direita_tras.duty_u16(0)

def mover_frente(pwm_value):
    motor_esquerda_frente.duty_u16(pwm_value)
    motor_esquerda_tras.duty_u16(0)
    motor_direita_frente.duty_u16(pwm_value)
    motor_direita_tras.duty_u16(0)

# Variáveis para controle de velocidade
max_speed_pwm = 65535   # Defina o limite de velocidade em PWM (0-65535)
current_pwm_value = 10  # Começa com 10
increment = 300  # Incremento de PWM a cada iteração
target_speed_pwm = max_speed_pwm  # Limite máximo de velocidade

# Inicializa o simulador de encoder
pin_sensor = 3  # Pino conectado ao sensor QRE
wheel_diameter = 5  # Diâmetro da roda em centímetros (ajuste conforme necessário)
encoder = EncoderSimulator(pin_sensor, wheel_diameter)

# Loop principal
try:
    while True:
        # Obtém os dados do sensor MPU6050
        data = get_mpu6050_data(i2c)
        
        # Aplica a calibração
        calibrated_accel = {
            'x': data['accel']['x'] - accel_offset['x'],
            'y': data['accel']['y'] - accel_offset['y'],
            'z': data['accel']['z'] - accel_offset['z']
        }
        
        calibrated_gyro = {
            'x': data['gyro']['x'] - gyro_offset['x'],
            'y': data['gyro']['y'] - gyro_offset['y'],
            'z': data['gyro']['z'] - gyro_offset['z']
        }
        
        # Verifica se houve uma mudança brusca na rotação
        if (abs(calibrated_gyro['x'] - previous_gyro['x']) > gyro_threshold or
            abs(calibrated_gyro['y'] - previous_gyro['y']) > gyro_threshold or
            abs(calibrated_gyro['z'] - previous_gyro['z']) > gyro_threshold):
            print("Mudança brusca na rotação detectada!")

            # Reinicia a contagem de PWM e começa a mover
            current_pwm_value = 6000  # Começa com 6000
            mover_frente(current_pwm_value)  # Começa a mover
            
            # Aumenta a velocidade gradativamente
            while current_pwm_value < target_speed_pwm:
                mover_frente(current_pwm_value)
                
                # Obtém e imprime a velocidade em RPM continuamente
                rpm = encoder.get_rpm()
                print("Velocidade de rotação (RPM):", rpm)
                
                # Verifica se a RPM atingiu ou ultrapassou 240
                if rpm >= 240:
                    print("RPM atingiu 240. Parando motores.")
                    parar()  # Para os motores
                    rpm = 0
                    print("Velocidade de rotação (RPM):", rpm)
                    break  # Sai do loop de aumento de velocidade
                
                utime.sleep(0.1)  # Aguarda um curto período antes de aumentar a velocidade
                current_pwm_value += increment
                if current_pwm_value > target_speed_pwm:
                    current_pwm_value = target_speed_pwm  # Garante que não ultrapasse o alvo
        
        # Atualiza as leituras anteriores
        previous_accel = calibrated_accel
        previous_gyro = calibrated_gyro
        
        utime.sleep(0.1)  # Adiciona um pequeno atraso para evitar sobrecarga no loop

except KeyboardInterrupt:
    # Se o programa for interrompido, pare os motores
    print("Programa interrompido. Parando motores.")
    parar()
