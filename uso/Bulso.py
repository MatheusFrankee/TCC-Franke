import time
import math
from machine import I2C, Pin, idle
from QMC5883 import QMC5883  
def get_direction(x, y):
    angle = math.atan2(y, x)
    angle = math.degrees(angle)
    if angle < 0:
        angle += 360

    # Ajuste as direções conforme necessário
    if angle >= 337.5 or angle < 22.5:
        return "Leste"
    elif angle >= 22.5 and angle < 67.5:
        return "Nordeste"
    elif angle >= 67.5 and angle < 112.5:
        return "norte"
    elif angle >= 112.5 and angle < 157.5:
        return "Noroeste"
    elif angle >= 157.5 and angle < 202.5:
        return "Oeste"
    elif angle >= 202.5 and angle < 247.5:
        return "Sudoeste"
    elif angle >= 247.5 and angle < 292.5:
        return "sul"
    elif angle >= 292.5 and angle < 337.5:
        return "Sudeste"

# Configuração do I2C
sda_pin = Pin(0)  # Pino SDA
scl_pin = Pin(1)  # Pino SCL
i2c = I2C(0, scl=scl_pin, sda=sda_pin, freq=400000)  # Frequência de 400kHz

# Inicializa o sensor QMC5883
sensor = QMC5883(i2c)

x_offset = -2333.5
y_offset = -2235.0
# Função para calibrar as leituras
def calibrate_reading(x, y):
    calibrated_x = x - x_offset
    calibrated_y = y - y_offset
    return calibrated_x, calibrated_y

# Loop para ler os dados do sensor
while True:
    try:
        # Lê os valores brutos do sensor
        x, y, z, temperature = sensor.readRaw()

        # Calibra as leituras
        calibrated_x, calibrated_y = calibrate_reading(x, y)

        # Obtém a direção
        direction = get_direction(calibrated_x, calibrated_y)

        # Exibe os valores lidos e a direção
        print("X: {}, Y: {}, Z: {}, Temperatura: {}°C, Direção: {}".format(x, y, z, temperature, direction))

        time.sleep(1)  # Espera 1 segundo antes da próxima leitura

    except Exception as e:
        print("Erro ao ler o sensor:", e)
        time.sleep(1)  # Espera um segundo antes de tentar novamente
