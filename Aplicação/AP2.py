from machine import Pin, I2C
from vl53l0x import VL53L0X
import time

# Configuração do I2C
sda_pin = Pin(0)  # Pino SDA
scl_pin = Pin(1)  # Pino SCL
i2c = I2C(0, scl=scl_pin, sda=sda_pin, freq=100000)  # Frequência de 100kHz

# Verifica os dispositivos conectados
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
    i2c.writeto(endereco_atual, bytearray([0x00]))  # Comando para ativar o sensor
    time.sleep(0.1)  # Aguarde um pouco para o sensor inicializar
    i2c.writeto(endereco_atual, bytearray([0x8A, novo_endereco]))  # Comando para mudar o endereço
    time.sleep(0.1)  # Aguarde um pouco para a mudança ser aplicada

# Inicializar sensores
tof1 = init_sensor(Xshut1, 0x2A)  # Inicializa o primeiro sensor com novo endereço
tof2 = init_sensor(Xshut2, 0x2B)  # Inicializa o segundo sensor com novo endereço

# Configurações do sensor
for tof in [tof1, tof2]:
    tof.set_measurement_timing_budget(40000)  # 40 ms
    tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)  # Pre-range
    tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)   # Final-range

# Configuração dos pinos dos motores
motor_esquerda_frente = Pin(8, Pin.OUT)
motor_esquerda_tras = Pin(7, Pin.OUT)
motor_direita_frente = Pin(9, Pin.OUT)
motor_direita_tras = Pin(10, Pin.OUT)

# Funções para controle do movimento
def parar():
    motor_esquerda_frente.off()
    motor_esquerda_tras.off()
    motor_direita_frente.off()
    motor_direita_tras.off()

def mover_frente():
    motor_esquerda_frente.on()
    motor_esquerda_tras.off()
    motor_direita_frente.on()
    motor_direita_tras.off()

def mover_tras():
    motor_esquerda_frente.off()
    motor_esquerda_tras.on()
    motor_direita_frente.off()
    motor_direita_tras.on()

def mover_esquerda():
    motor_esquerda_frente.off()
    motor_esquerda_tras.on()
    motor_direita_frente.on()
    motor_direita_tras.off()

def mover_direita():
    motor_esquerda_frente.on()
    motor_esquerda_tras.off()
    motor_direita_frente.off()
    motor_direita_tras.on()

# Loop principal
try:
    while True:
        # Medir com os sensores
        para1 = tof1.ping()
        para2 = tof2.ping()
        
        distance1 = tof1.ping()
        distance2 = tof2.ping()

        print(distance1)  # Ajuste conforme necessário
        print(distance2)  # Ajuste conforme necessário

        # Modo de segurança
        if para1 < 100 and para2 < 100:
            print("Modo de segurança ativado!")
            parar()
            continue

            # Lógica do robô seguidor de alvo
        if distance1 > 105 and distance2 > 105:
            # Ambos os sensores detectam o alvo
            print("Avançando em linha reta.")
            mover_frente()
        elif distance1 > 105 and distance2 < 100:
            # Apenas o sensor esquerdo detecta o alvo
            print("Ajustando para a esquerda.")           
            mover_direita()
        elif distance2 > 105 and distance1 < 100:
            # Apenas o sensor direito detecta o alvo
            print("Ajustando para a direita.")
            mover_esquerda()
        else:
            # Nenhum alvo detectado
            print("Parado, nenhum alvo detectado.")
            parar()

        time.sleep(0.1)  # Aguarde um pouco entre as medições

except KeyboardInterrupt:
    parar()  # Parar os motores ao interromper o programa
    print("Programa interrompido.")
