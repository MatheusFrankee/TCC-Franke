import time
import struct
from machine import idle

class QMC5883:
    # Endereço I2C padrão
    ADDR = 0x0D

    # QMC5883 = Registro = números
    X_LSB = 0
    X_MSB = 1
    Y_LSB = 2
    Y_MSB = 3
    Z_LSB = 4
    Z_MSB = 5
    STATUS = 6
    T_LSB = 7
    T_MSB = 8
    CONFIG = 9
    CONFIG2 = 10
    RESET = 11
    CHIP_ID = 13

    # Valores de bits para o registro STATUS
    STATUS_DRDY = 1
    STATUS_OVL = 2
    STATUS_DOR = 4

    # Valores de sobreamostragem para o registro CONFIG
    CONFIG_OS512 = 0b00000000
    CONFIG_OS256 = 0b01000000
    CONFIG_OS128 = 0b10000000
    CONFIG_OS64  = 0b11000000

    # Valores de intervalo para o registro CONFIG
    CONFIG_2GAUSS = 0b00000000
    CONFIG_8GAUSS = 0b00010000

    # Valores de taxa para o registro CONFIG
    CONFIG_10HZ = 0b00000000
    CONFIG_50HZ = 0b00000100
    CONFIG_100HZ = 0b00001000
    CONFIG_200HZ = 0b00001100

    # Valores de modo para o registro CONFIG
    CONFIG_STANDBY = 0b00000000
    CONFIG_CONT = 0b00000001

    def __init__(self, i2c):
        self.i2c = i2c
        self.oversampling = QMC5883.CONFIG_OS64
        self.range = QMC5883.CONFIG_2GAUSS
        self.rate = QMC5883.CONFIG_100HZ
        self.mode = QMC5883.CONFIG_CONT
        self.reset()

    def reconfig(self):
        config_value = self.oversampling | self.range | self.rate | self.mode
        print("{0:b}".format(config_value))
        self.i2c.writeto_mem(QMC5883.ADDR, QMC5883.CONFIG, bytes([config_value]))

    def reset(self):
        self.i2c.writeto_mem(QMC5883.ADDR, QMC5883.RESET, bytes([0x01]))  
        time.sleep(0.1)
        self.reconfig()  # Reconfigura após o reset
        time.sleep(0.01)

    def setOversampling(self, x):
        self.oversampling = x
        self.reconfig()

    def setRange(self, x):
        self.range = x
        self.reconfig()

    def setSamplingRate(self, x):
        self.rate = x
        self.reconfig()

    def ready(self):
        status = self.i2c.readfrom_mem(QMC5883.ADDR, QMC5883.STATUS, 1)[0]

        
        if (status == QMC5883.STATUS_DOR):
            print("fail")
            return QMC5883.STATUS_DRDY

        return status & QMC5883.STATUS_DRDY

    def readRaw(self):
        while not self.ready():
            idle()
            pass

        # Ler dados do sensor
        register = self.i2c.readfrom_mem(QMC5883.ADDR, QMC5883.X_LSB, 9)

        # Converte os valores do eixo para signed Short antes de retornar
        x, y, z, status, t = struct.unpack('<hhhBh', register)

        return (x, y, z, t)
