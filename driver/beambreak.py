from machine import PWM, ADC, Pin


class BeamBreak:
    """Micropython Debounced GPIO Input Class"""

    def __init__(self, sensor_pin, led_pin, led_freq=100_000, led_brightness=65535):
        self.__snsr = ADC(Pin(sensor_pin))
        self.__led = PWM(Pin(led_pin), freq=led_freq, duty_u16=led_brightness)

    def read(self):
        return self.__snsr.read_u16()

    def brightness(self, brightness):
        self.__led.duty_u16(brightness)
