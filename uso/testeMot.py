from machine import Pin
import time

# Configuração dos pinos dos motores
motor_esquerda_frente = Pin(7, Pin.OUT)
motor_esquerda_tras = Pin(8, Pin.OUT)
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

# Teste de movimentação
try:
    while True:
        mover_frente()  # Mover para frente
        time.sleep(2)   # Mover para frente por 2 segundos
        parar()         # Parar
        time.sleep(1)   # Esperar 1 segundo
        mover_tras()    # Mover para trás
        time.sleep(2)   # Mover para trás por 2 segundos
        parar()         # Parar
        time.sleep(1)   # Esperar 1 segundo
except KeyboardInterrupt:
    parar()  # Parar os motores ao interromper o programa