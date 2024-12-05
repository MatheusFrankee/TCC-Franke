from machine import Pin
from time import sleep

# Configuração do pino onde o sensor QRE está conectado
sensor_qre = Pin(3, Pin.IN)  # Substitua pelo número do pino que você usou

while True:
    # Lê o valor do sensor
    valor = sensor_qre.value()
    
    # Determina se a superfície é preta ou branca
    if valor == 0:
        print("Superfície Branca Detectada")
    else:
        print("Superfície Preta Detectada")
    
    # Aguarda um pequeno intervalo antes de ler novamente
    sleep(0.1)