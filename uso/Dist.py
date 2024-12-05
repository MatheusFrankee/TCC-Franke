from machine import Pin, I2C
from vl53l0x import VL53L0X
import time

print("Setting up I2C")
# Configuração do I2C
sda_pin = Pin(0)  # Pino SDA
scl_pin = Pin(1)  # Pino SCL
i2c = I2C(0, scl=scl_pin, sda=sda_pin, freq=100000)  # Frequência de 100kHz

# Verifique os dispositivos conectados
print("Dispositivos encontrados:", i2c.scan())

# Pinos XSHUT
Xshut1 = Pin(16, Pin.OUT)
Xshut2 = Pin(17, Pin.OUT)

# Função para inicializar um sensor
def init_sensor(xshut_pin, new_address):
    xshut_pin.value(0)  # Desligar o sensor
    time.sleep(0.1)     # Aguardar 100ms
    xshut_pin.value(1)  # Ligar o sensor
    time.sleep(0.1)     # Aguardar 100ms para inicialização

    # Mudar o endereço I2C
    mudar_endereco(i2c, 0x29, new_address)

    # Criar objeto do sensor
    sensor = VL53L0X(i2c, new_address)
    return sensor

# Função para mudar o endereço I2C
def mudar_endereco(i2c, endereco_atual, novo_endereco):
    # Ative o sensor
    i2c.writeto(endereco_atual, bytearray([0x00]))  # Comando para ativar o sensor
    time.sleep(0.1)  # Aguarde um pouco para o sensor inicializar

    # Mude o endereço
    i2c.writeto(endereco_atual, bytearray([0x8A, novo_endereco]))  # Comando para mudar o endereço
    time.sleep(0.1)  # Aguarde um pouco para a mudança ser aplicada

# Inicializar sensores
tof1 = init_sensor(Xshut1, 0x2A)  # Inicializa o primeiro sensor com novo endereço
tof2 = init_sensor(Xshut2, 0x2B)  # Inicializa o segundo sensor com novo endereço

# Configurações do sensor
for tof in [tof1, tof2]:
    # Define o tempo de medição
    tof.set_measurement_timing_budget(40000)  # 40 ms
    tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)  # Pre-range
    tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)   # Final-range

while True:
    # Medir com o primeiro sensor
    distance1 = tof1.ping()
    print("Sensor 1: ", distance1 - 50, "mm")  # Ajuste conforme necessário

    # Medir com o segundo sensor
    distance2 = tof2.ping()
    print("Sensor 2: ", distance2 - 50, "mm")  # Ajuste conforme necessário

    time.sleep(0.1)  # Aguarde 1 segundo entre as medições