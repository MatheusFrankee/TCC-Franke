import time
import math
from machine import I2C, Pin
from QMC5883 import QMC5883

# Configuração dos pinos dos motores
motor_left_forward = Pin(8, Pin.OUT)
motor_left_backward = Pin(7, Pin.OUT)
motor_right_forward = Pin(9, Pin.OUT)
motor_right_backward = Pin(10, Pin.OUT)

# Funções para controle do movimento
def stop():
    motor_left_forward.off()
    motor_left_backward.off()
    motor_right_forward.off()
    motor_right_backward.off()

def turn_right():
    motor_left_forward.on()
    motor_left_backward.off()
    motor_right_forward.off()
    motor_right_backward.on()

def turn_left():
    motor_left_forward.off()
    motor_left_backward.on()
    motor_right_forward.on()
    motor_right_backward.off()

def get_direction(x, y):
    angle = math.atan2(y, x)
    angle = math.degrees(angle)
    if angle < 0:
        angle += 360

    # Ajuste as direções conforme necessário
    if angle >= 337.5 or angle < 22.5:
        return "Leste"
    elif angle >= 22.5 and angle < 50:
        return "Nordeste"
    elif angle >= 50 and angle < 250:
        return "Norte"
    elif angle >= 112.5 and angle < 157.5:
        return "Noroeste"
    elif angle >= 157.5 and angle < 202.5:
        return "Oeste"
    elif angle >= 202.5 and angle < 247.5:
        return "Sudoeste"
    elif angle >= 2250 and angle < 292.5:
        return "Sul"
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
try:
    while True:
        # Lê os valores brutos do sensor
        x, y, z, temperature = sensor.readRaw()

        # Calibra as leituras
        calibrated_x, calibrated_y = calibrate_reading(x, y)

        # Obtém a direção
        direction = get_direction(calibrated_x, calibrated_y)

        # Verifica se está apontando para o norte
        if direction == "Norte":
            print("O robô está apontando para o norte. Parando.")
            stop()  # Para o robô se estiver alinhado ao norte
        else:
            # Se não estiver apontando para o norte, gira em direção ao norte
            if direction in ["Leste", "Sudeste", "Sul", "Sudoeste"]:
                print("não esta pro norte.")
                turn_left()
            else:
                print("não esta pro norte.")
                turn_right()

        time.sleep(1)  # Espera 1 segundo antes da próxima leitura

except KeyboardInterrupt:
    stop()  # Para os motores ao interromper o programa
    
    
    
    
    
    
    
    
    
    
