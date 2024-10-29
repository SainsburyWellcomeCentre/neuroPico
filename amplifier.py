from machine import I2C
from micropython import const
from .driver.ad5259 import AD5259

PRE_GAIN = const(0.28)
RESISTOR_A = const(100_000)
RESISTOR_B = const(100)


class Amplifier:

    def __init__(self, i2c: I2C, addr):
        self.vr = AD5259(i2c, addr)

    def setGain(self, val):
        ratio = val / PRE_GAIN - 1
        r = (RESISTOR_A / ratio) - RESISTOR_B
        dig = round(r / self.vr.resistance * 256)
        self.vr.write(dig)
