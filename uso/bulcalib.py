import time
import math
from machine import I2C, Pin, idle
from QMC5883 import QMC5883  

# Configuração do I2C
sda_pin = Pin(0)  # Pino SDA
scl_pin = Pin(1)  # Pino SCL
i2c = I2C(0, scl=scl_pin, sda=sda_pin, freq=400000)  # Frequência de 400kHz

# Inicializa o sensor QMC5883
sensor = QMC5883(i2c)

# Coleta de dados para calibração
x_values = []
y_values = []

# Coletar dados para calibração
print("Gire o sensor 360 graus para calibrar...")
for _ in range(500):  # Coletar 500 leituras
    x, y, z, temperature = sensor.readRaw()
    x_values.append(x)
    y_values.append(y)
    time.sleep(0.01)  # Pequena pausa entre as leituras

# Calcular os valores máximos e mínimos
x_min = min(x_values)
x_max = max(x_values)
y_min = min(y_values)
y_max = max(y_values)

# Calcular o offset
x_offset = (x_max + x_min) / 2
y_offset = (y_max + y_min) / 2

print("Offset X:", x_offset)
print("Offset Y:", y_offset)
