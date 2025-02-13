from machine import Pin, I2C, UART
from micropython import const
from .driver.ws2812c import WS2812C
from .utilty.debounce import DebouncedInput
from .motor import Motor
from .port import AnalogPort, DigitalPort
from .amplifier import Amplifier


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

    PIN_CLK_IN = const(13)
    PIN_CLK_nEN = const(12)

    PIN_PORT1_A = const(17)
    PIN_PORT1_B = const(26)
    PIN_PORT2_A = const(18)
    PIN_PORT2_B = const(27)
    PIN_PORT3_A = const(21)
    PIN_PORT3_B = const(28)
    PIN_PORT4_A = const(22)
    PIN_PORT4_B = const(29)

    ADDR_AMP1 = const(0x18)
    ADDR_AMP2 = const(0x4C)
    ADDR_AMP3 = const(0x1A)
    ADDR_AMP4 = const(0x4E)

    PIN_PORT5_A = const(2)
    PIN_PORT5_B = const(3)
    PIN_PORT5_C = const(0)
    PIN_PORT5_D = const(1)
    PIN_PORT6_A = const(8)
    PIN_PORT6_B = const(9)
    PIN_PORT6_C = const(10)
    PIN_PORT6_D = const(11)

    PIN_LVL_SWITCH_5 = const(14)
    PIN_LVL_SWITCH_6 = const(15)

    CLK_SPEED = const(100_000)

    USB_CLOCK = const(0)
    EXT_CLOCK = const(1)

    def __init__(self):
        self.LED = WS2812C(Pin(self.PIN_LED))
        self.BTNA = DebouncedInput(self.PIN_BTNA, DebouncedInput.High, debounce_ms=20)
        self.BTNB = DebouncedInput(self.PIN_BTNB, DebouncedInput.High, debounce_ms=20)
        self.I2C = I2C(id=0, scl=self.PIN_SCL, sda=self.PIN_SDA, freq=400_000)
        self.MOTOR = Motor(
            pwm_pin_a=self.PIN_MOTOR_A,
            pwm_pin_b=self.PIN_MOTOR_B,
            enable_pin=self.PIN_MOTOR_EN,
            encoder_pin_a=self.PIN_ENC_A,
            encoder_pin_b=self.PIN_ENC_B,
            i2c=self.I2C,
        )
        self.PORT1 = AnalogPort(self.PIN_PORT1_A, self.PIN_PORT1_B, Amplifier(self.I2C, self.ADDR_AMP1))
        self.PORT2 = AnalogPort(self.PIN_PORT2_A, self.PIN_PORT2_B, Amplifier(self.I2C, self.ADDR_AMP2))
        self.PORT3 = AnalogPort(self.PIN_PORT3_A, self.PIN_PORT3_B, Amplifier(self.I2C, self.ADDR_AMP3))
        self.PORT4 = AnalogPort(self.PIN_PORT4_A, self.PIN_PORT4_B, Amplifier(self.I2C, self.ADDR_AMP4))
        self.PORT5 = DigitalPort(
            self.PIN_PORT5_A, self.PIN_PORT5_B, self.PIN_PORT5_C, self.PIN_PORT5_D, self.PIN_LVL_SWITCH_5, 0, 0
        )
        self.PORT6 = DigitalPort(
            self.PIN_PORT6_A, self.PIN_PORT6_B, self.PIN_PORT6_C, self.PIN_PORT6_D, self.PIN_LVL_SWITCH_6, 1, 1
        )
        self.PORT7 = self.I2C

        self.CLK_IN = UART(0, rx=self.PIN_CLK_IN, baudrate=self.CLK_SPEED)
        self.CLK_nEN = Pin(self.PIN_CLK_nEN, Pin.OUT, value=1)

    def setClockSource(self, src=EXT_CLOCK):
        if src is self.EXT_CLOCK:
            en = 1
        elif src is self.USB_CLOCK:
            en = 10
        self.CLK_nEN.value(en)
