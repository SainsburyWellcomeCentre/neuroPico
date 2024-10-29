from machine import I2C
import time
from micropython import const


ADDRESSES = [const(24), const(26), const(76), const(78)]
R_RDAC = const(0)
R_EEPROM = const(0x10)
R_ROM2DAC = const(0x50)
R_DAC2ROM = const(0x60)
R_TOLERANCE = const(0x3E)
RESISTANCE = const(100_000)


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
        self.resistance = RESISTANCE * (1 + self._read_tolerance())

    def write(self, val):
        self._write_dat(R_RDAC, bytearray([val]))

    def write2ROM(self, val):
        self._write_dat(R_EEPROM, bytearray([val]))

    def _read_tolerance(self):
        temp = self._read_dat(R_TOLERANCE, 2)
        sign = (temp[0] & 0x80) >> 7
        val = ((temp[0] & 0x7F) << 8) + temp[1]
        val /= 25600
        val = (-1 * val) if sign else val
        return val

    def _read_dat(self, mem_addr, length):
        return self.i2c.readfrom_mem(self.ADDR, mem_addr, length)

    def _write_dat(self, mem_addr, buf):
        self.i2c.writeto_mem(self.ADDR, mem_addr, buf)
