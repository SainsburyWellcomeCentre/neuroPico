from machine import I2C
import time
from micropython import const


ADDRESS = const(41)
ADDRSIZE = const(16)
R_FIRMWARE__ENABLE = const(0x0085)
R_POWER_MANAGEMENT__GO1_POWER_FORCE = const(0x0083)
R_PATCH__OFFSET_0 = const(0x0476)
R_PATCH__ADDRESS_0 = const(0x0496)
R_PATCH__JMP_ENABLES = const(0x0472)
R_PATCH__DATA_ENABLES = const(0x0474)
R_PATCH__CTRL = const(0x0470)
R_GPIO__TIO_HV_STATUS = const(0x0031)
R_SYSTEM_RESULTS = const(0x0088)
R_CONFIG_INDEX = const(0x0024)
R_SYSTEM_INTERRUPT_CLEAR = const(0x0086)
R_CONFIG_LEN = const(100)
GAIN_FACTOR = const(2011)


class VL53LX:
    # 100 bytes default configuration
    CONFIG_DATA = bytearray(
        [
            0x0A,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x11,
            0x02,
            0x00,
            0x02,
            0x08,
            0x00,
            0x08,
            0x10,
            0x01,
            0x01,
            0x00,
            0x00,
            0x00,
            0x00,
            0xFF,
            0x00,
            0x02,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x20,
            0x0B,
            0x00,
            0x00,
            0x02,
            0x0D,
            0x21,
            0x00,
            0x00,
            0x01,
            0x00,
            0x00,
            0x00,
            0x00,
            0x8C,
            0x00,
            0x00,
            0x38,
            0xFF,
            0x01,
            0x00,
            0x1A,
            0x00,
            0x20,
            0x01,
            0xCC,
            0x0B,
            0x01,
            0xF5,
            0x09,
            0x00,
            0x3C,
            0x00,
            0x80,
            0x08,
            0x78,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x01,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x02,
            0x0B,
            0x09,
            0x0A,
            0x0A,
            0x01,
            0x00,
            0x02,
            0xC7,
            0xFF,
            0xDB,
            0x02,
            0x01,
            0x00,
            0x01,
            0x01,
            0x21,
        ]
    )

    def __init__(self, i2c: I2C):
        self.i2c = i2c
        self._load_patch()
        self._dev_init()

    def _read_dat(self, mem_addr, length):
        return self.i2c.readfrom_mem(ADDRESS, mem_addr, length, addrsize=ADDRSIZE)

    def _write_dat(self, mem_addr, buf):
        self.i2c.writeto_mem(ADDRESS, mem_addr, buf, addrsize=ADDRSIZE)

    def _load_patch(self):
        self._write_dat(R_FIRMWARE__ENABLE, b"\x00")  # firmware disable
        self._write_dat(R_POWER_MANAGEMENT__GO1_POWER_FORCE, b"\x01")  # power force enable

        # load patch
        self._write_dat(R_PATCH__OFFSET_0, bytearray([0x29, 0xC9, 0x0E, 0x40, 0x28, 0x00]))
        self._write_dat(R_PATCH__ADDRESS_0, bytearray([0x03, 0x6D, 0x03, 0x6F, 0x07, 0x29]))
        self._write_dat(R_PATCH__JMP_ENABLES, bytearray([0x00, 0x07]))
        self._write_dat(R_PATCH__DATA_ENABLES, bytearray([0x00, 0x07]))
        self._write_dat(R_PATCH__CTRL, b"\x01")

        self._write_dat(R_FIRMWARE__ENABLE, b"\x01")  # firmware enable again

    def _dev_init(self):

        self._write_dat(0x0024, self.CONFIG_DATA)

    def read_mm(self):
        while not self._is_data_ready():
            time.sleep_us(100)

        raw = self._read_dat(R_SYSTEM_RESULTS + 14, 2)
        self._clear_interrput()
        return (((raw[0] << 8) + raw[1]) * GAIN_FACTOR + 0x0400) / 0x0800

    def _is_data_ready(self):
        flag = int.from_bytes(self._read_dat(R_GPIO__TIO_HV_STATUS, 1), "big") & 0x01
        return True if flag == 0 else False

    def _clear_interrput(self):
        self._write_dat(R_SYSTEM_INTERRUPT_CLEAR, b"\x01")
