from encoder import EncoderSimulator
import utime

# Parâmetros do sensor e do diâmetro da roda
pin_sensor = 3  # Pino conectado ao sensor QRE
wheel_diameter = 5  # Diâmetro da roda em centímetros (ajuste conforme necessário)

# Cria o simulador de encoder
encoder = EncoderSimulator(pin_sensor, wheel_diameter)

# Loop principal para monitorar RPM
while True:
    rpm = encoder.get_rpm()
    print("Velocidade de rotação (RPM):", rpm)
    utime.sleep(1)  # Atualiza a leitura a cada 1 segundo
