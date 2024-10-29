from machine import I2C
from micropython import const

ADDRESS = const(77)
ENABLE_MASK = const(0x00)
DISABLE_MASK = const(0x30)


class DAC5571:

    def __init__(self, i2c: I2C):
        self.i2c = i2c
        self.disable()

    def set(self, val: int):
        val = 0 if val < 0 else val
        val &= 0xFF
        ms = (val & 0xF0) >> 4 + ENABLE_MASK
        ls = (val & 0x0F) << 4
        self._write_dat(bytearray([ms, ls]))

    def disable(self):
        self._write_dat(bytearray([DISABLE_MASK, 0]))

    def _write_dat(self, buf):
        self.i2c.writeto(ADDRESS, buf)
