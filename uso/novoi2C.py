from machine import I2C, Pin
import time

# Inicializa o barramento I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Ajuste os pinos conforme necessário

# Endereço atual do sensor
endereco_atual = 0x29 # Endereço padrão do VL53L1X

# Novo endereço que você deseja definir
novo_endereco = 0x2A  # Exemplo de novo endereço

# Função para mudar o endereço I2C
def mudar_endereco(i2c, endereco_atual, novo_endereco):
    # Ative o sensor
    i2c.writeto(endereco_atual, bytearray([0x00]))  # Comando para ativar o sensor (ajuste conforme necessário)
    time.sleep(0.1)  # Aguarde um pouco para o sensor inicializar

    # Mude o endereço
    i2c.writeto(endereco_atual, bytearray([0x8A, novo_endereco]))  # Comando para mudar o endereço
    time.sleep(0.1)  # Aguarde um pouco para a mudança ser aplicada

# Chame a função para mudar o endereço
mudar_endereco(i2c, endereco_atual, novo_endereco)

# Verifique se o novo endereço está ativo
dispositivos = i2c.scan()
print("Dispositivos encontrados:", dispositivos)
