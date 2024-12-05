from machine import Pin, I2C

# Configuração do I2C
sda = Pin(0)  # Pino SDA
scl = Pin(1)  # Pino SCL
i2c = I2C(0, sda=sda, scl=scl)

# Realiza a varredura dos dispositivos I2C
dispositivos = i2c.scan()

# Exibe os endereços dos dispositivos encontrados
if dispositivos:
    print("Dispositivos I2C encontrados:", [hex(endereco) for endereco in dispositivos])
else:
    print("Nenhum dispositivo I2C encontrado.")

