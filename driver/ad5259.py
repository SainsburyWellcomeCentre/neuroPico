from machine import I2C
import time
from micropython import const


ADDRESSES = [const(24), const(26), const(76), const(78)]


class AD5259:

    def __init__(self, i2c: I2C, addr):
        isAddrValid = False
        for address in ADDRESSES:
            if address == addr:
                isAddrValid = True
                self.ADDR = addr

        if not isAddrValid:
            raise ValueError("Invalid ad5259 address: " + addr)
        self.i2c = i2c

    def read(self):
        ang_raw = self.__read_dat(self.ANGLE_RAW, 2)
        ang = (ang_raw[0] * 256 + ang_raw[1]) * 360 / 4096
        return round(ang, 3)

    def __read_dat(self, mem_addr, length):
        return self.i2c.readfrom_mem(self.ADDR, mem_addr, length)

    def __write_dat(self, mem_addr, buf):
        self.i2c.writeto_mem(self.ADDR, mem_addr, buf)
