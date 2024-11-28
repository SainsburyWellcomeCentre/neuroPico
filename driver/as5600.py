from machine import I2C
import time
from micropython import const

ADDRESS = const(54)
R_ANGLE_RAW = const(0x0C)
R_ANGLE = const(0x0E)
R_MAGNITUDE = const(0x1B)


class AS5600:

    def __init__(self, i2c: I2C):
        self.i2c = i2c

    def read_angle(self):
        return self._12_bit_decode(self._read_dat(R_ANGLE, 2))

    def read_angle_raw(self):
        return self._12_bit_decode(self._read_dat(R_ANGLE_RAW, 2))

    def read_mag(self):
        return self._12_bit_decode(self._read_dat(R_MAGNITUDE, 2))

    def _12_bit_decode(self, buf):
        return buf[0] * 256 + buf[1]

    def _read_dat(self, mem_addr, length):
        return self.i2c.readfrom_mem(ADDRESS, mem_addr, length)

    def _write_dat(self, mem_addr, buf):
        self.i2c.writeto_mem(ADDRESS, mem_addr, buf)
