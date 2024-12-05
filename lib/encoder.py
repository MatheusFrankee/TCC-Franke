from machine import Pin, Timer
import utime

class EncoderSimulator:
    def __init__(self, pin_num, wheel_diameter):
        self.sensor = Pin(pin_num, Pin.IN)
        self.wheel_diameter = wheel_diameter
        self.last_time = utime.ticks_us()
        self.rotation_time = None
        self.rpm = 0
        self.state = "waiting_line"  # Estado inicial

        # Timer para calcular RPM periodicamente
        self.timer = Timer()
        self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.calculate_rpm)

        # Configura interrupção no sensor
        self.sensor.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.handle_sensor)

    def handle_sensor(self, pin):
        """Manipula a interrupção de borda de subida/descida para detectar linhas."""
        current_time = utime.ticks_us()
        elapsed_time = utime.ticks_diff(current_time, self.last_time)

        # Detecta a linha preta passando pela posição do sensor
        if pin.value() == 0 and self.state == "waiting_line":
            self.rotation_time = elapsed_time
            self.last_time = current_time
            self.state = "measuring"  # Estado para medir a próxima linha

        # Detecta a segunda linha preta para concluir uma volta
        elif pin.value() == 0 and self.state == "measuring":
            self.rotation_time = elapsed_time
            self.last_time = current_time
            self.state = "waiting_line"  # Reinicia o ciclo de detecção

    def calculate_rpm(self, timer):
        """Calcula a velocidade em RPM com base no tempo de rotação."""
        if self.rotation_time:
            seconds_per_rotation = self.rotation_time / 1_000_000
            self.rpm = (60 / seconds_per_rotation) if seconds_per_rotation > 0 else 0

    def get_rpm(self):
        """Retorna a velocidade em RPM calculada."""
        return self.rpm
