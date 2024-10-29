from machine import I2C
import time
from micropython import const

ADDRESS = const(54)
R_ANGLE_RAW = const(12)


class AS5600:

    def __init__(self, i2c: I2C):
        self.i2c = i2c

    def readAngle(self):
        ang_raw = self._read_dat(R_ANGLE_RAW, 2)
        ang = (ang_raw[0] * 256 + ang_raw[1]) * 360 / 4096
        return round(ang, 3)

    def _read_dat(self, mem_addr, length):
        return self.i2c.readfrom_mem(ADDRESS, mem_addr, length)

    def _write_dat(self, mem_addr, buf):
        self.i2c.writeto_mem(ADDRESS, mem_addr, buf)
