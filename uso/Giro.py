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
    
    # Exibe a temperatura em graus Celsius
    print("Temperatura: {:.2f} °C".format(data['temp']).replace('.', ','))  # Substitui '.' por ',' para o padrão brasileiro
    
    # Exibe a aceleração calibrada em g (gravitacional) para os eixos X, Y e Z
    print("Aceleração: X: {:.2f} g, Y: {:.2f} g, Z: {:.2f} g".format(calibrated_accel['x'], calibrated_accel['y'], calibrated_accel['z']).replace('.', ','))
    
    # Exibe a taxa de rotação (giroscópio) calibrada em graus por segundo para os eixos X, Y e Z
    print("Giroscópio: X: {:.2f} °/s, Y: {:.2f} °/s, Z: {:.2f} °/s".format(calibrated_gyro['x'], calibrated_gyro['y'], calibrated_gyro['z']).replace('.', ','))
    
    # Aguarda 0.5 segundos antes da próxima leitura
    utime.sleep(1)
