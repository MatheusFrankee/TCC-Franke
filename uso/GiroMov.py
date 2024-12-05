from machine import Pin, I2C
import utime
from MPU6050 import init_mpu6050, get_mpu6050_data

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

# Loop principal para leitura contínua dos dados do sensor
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
    
    # Verifica se houve uma mudança brusca na aceleração
    if (abs(calibrated_accel['x'] - previous_accel['x']) > accel_threshold or
        abs(calibrated_accel['y'] - previous_accel['y']) > accel_threshold or
        abs(calibrated_accel['z'] - previous_accel['z']) > accel_threshold):
        print("Mudança brusca na aceleração detectada!")
        utime.sleep(1)

    # Verifica se houve uma mudança brusca na rotação
    if (abs(calibrated_gyro['x'] - previous_gyro['x']) > gyro_threshold or
        abs(calibrated_gyro['y'] - previous_gyro['y']) > gyro_threshold or
        abs(calibrated_gyro['z'] - previous_gyro['z']) > gyro_threshold):
        print("Mudança brusca na rotação detectada!")
        utime.sleep(1)
    # Atualiza as leituras anteriores
    previous_accel = calibrated_accel
    previous_gyro = calibrated_gyro
    
   

