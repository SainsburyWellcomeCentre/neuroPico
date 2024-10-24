from machine import Pin, I2C
from micropython import const
from .driver.ws2812c import WS2812C
from .utilty.debounce import DebouncedInput
from .motor import Motor

class NeuroPico:

    PIN_LED = const(16)

    PIN_BTNA = const(20)
    PIN_BTNB = const(19)

    PIN_SCL = const(25)
    PIN_SDA = const(24)

    PIN_MOTOR_A = const(6)
    PIN_MOTOR_B = const(7)

    PIN_ENC_A = const(4)
    PIN_ENC_B = const(5)

    PIN_MOTOR_EN = const(23)

    def __init__(self):
        self.LED = WS2812C(Pin(self.PIN_LED))
        self.BTNA = DebouncedInput(self.PIN_BTNA, DebouncedInput.High)
        self.BTNB = DebouncedInput(self.PIN_BTNB, DebouncedInput.High)
        self.I2C = I2C(id=0, scl=self.PIN_SCL, sda=self.PIN_SDA, freq=400_000)
        self.MOTOR = Motor(pwm_pin_a=self.PIN_MOTOR_A, pwm_pin_b=self.PIN_MOTOR_B, enable_pin=self.PIN_MOTOR_EN, encoder_pin_a=self.PIN_ENC_A, encoder_pin_b=self.PIN_ENC_B)
        # self.PORTA =
        # self.PORTB =
        # self.PORTC =
        # self.PORTD =
        # self.PORTE =
        # self.PORTF =
        # self.PORTG =
