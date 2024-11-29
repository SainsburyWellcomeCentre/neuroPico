from machine import Pin, ADC, PWM, SPI, UART
from micropython import const
from .amplifier import Amplifier


class Port:
    PIN_A = const(0)
    PIN_B = const(1)
    PIN_C = const(2)
    PIN_D = const(3)

    DIG = const(4)
    ANG = const(5)
    # UART = const(6)
    # SPI = const(7)
    # I2C = const(8)

    def __init__(self, pin_num_a, pin_num_b):
        self._pin_list = [pin_num_a, pin_num_b]
        self.mode = Port.DIG

    def value(self, pin_index=1, logic=-1):
        self._index_check(pin_index)

        if logic == -1:
            return self._read(pin_index)
        else:
            self._set(pin_index, logic)
            return logic

    def toggle(self, pin_index):
        self._index_check(pin_index)

        pin_temp = Pin(self._pin_list[pin_index], Pin.OUT)
        pin_temp.toggle()

    def _read(self, pin_index):
        if self.mode == Port.DIG:
            pin_temp = Pin(self._pin_list[pin_index], Pin.IN)
            return pin_temp.value()
        elif self.mode == Port.ANG:
            pin_temp = ADC(self._pin_list[self.PIN_B])
            return pin_temp.read_u16()
        else:
            return -1

    def _set(self, pin_index, logic):
        if self.mode == Port.DIG:
            pin_temp = Pin(self._pin_list[pin_index], Pin.OUT)
        elif self.mode == Port.ANG:
            pin_temp = Pin(self._pin_list[self.PIN_A], Pin.OUT)

        pin_temp.value(logic)

    def _index_check(self, index):
        if index < 0 or index > len(self._pin_list):
            raise ValueError("index out of range.")


class AnalogPort(Port):
    def __init__(self, pin_num_a, pin_num_b, amp: Amplifier, freq=100_000):
        super().__init__(pin_num_a, pin_num_b)
        self._amp = amp
        self.freq = freq
        self.duty = 0
        self.setGain(1)
        self.setPWM(0)

    def setGain(self, gain):
        if gain < 0:
            raise ValueError("gain value cannot be negative.")
        self._amp.setGain(gain)

    def setPWM(self, duty):
        if duty < 0:
            raise ValueError("duty rate cannot be negative.")
        pwm = PWM(Pin(self._pin_list[Port.PIN_A]), freq=self.freq, duty_u16=0)
        pwm.duty_u16(duty)
        self.duty = duty


class DigitalPort(Port):
    LOGIC_3V3 = const(0)
    LOGIC_5V = const(1)

    # TODO: fix spi and uart initailisation
    def __init__(self, pin_num_a, pin_num_b, pin_num_c, pin_num_d, pin_level_switch, spi_id, uart_id):
        super().__init__(pin_num_a, pin_num_b)
        self._pin_list.append([pin_num_c, pin_num_d])
        self._lvl_switch = Pin(pin_level_switch, Pin.OUT, 0)
        # self.spi = SPI(spi_id)
        # self.uart = UART(uart_id)
        self.sck = self.cts = pin_num_a
        self.mosi = self.rts = pin_num_b
        self.miso = self.tx = pin_num_c
        self.cs = self.rx = pin_num_d

    def setLogicLevel(self, Level):
        self._lvl_switch.value(Level)
