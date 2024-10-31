from machine import Pin, Timer
from micropython import const
from .utilty.encoder import Encoder
from .utilty.debounce import DebouncedInput
from .driver.m2619s import M2619S
from .driver.dac5571 import DAC5571
from .utilty.pid import PID

CW = const(0)
CCW = const(1)
STOP = const(2)


class Motor(M2619S):
    def __init__(self, pwm_pin_a, pwm_pin_b, enable_pin, encoder_pin_a, encoder_pin_b, i2c, pwm_freq=10_000):
        super().__init__(pwm_pin_a, pwm_pin_b, pwm_freq)

        self._vm_ctrl = VoltageController(i2c)

        self.pid = PIDcontroller(self)

        self.encoder = Encoder(encoder_pin_a, encoder_pin_b)

        self._enable = Pin(enable_pin, Pin.OUT, value=0)
        self.status = STOP
        self._limiter_a = None
        self._limiter_b = None

    def setSpeed(self, speed):
        direction = CW if speed > 0 else CCW

        if self._limiter_a and direction == CW and self._limiter_a.value == 0:
            self.set(0)
            self.status = STOP
        elif self._limiter_b and direction == CCW and self._limiter_b.value == 0:
            self.set(0)
            self.status = STOP
        elif speed:
            self.set(speed)
            self.status = direction
        else:
            self.set(speed)
            self.status = STOP

    def setVoltage(self, voltage):
        self._vm_ctrl.setVoltage(voltage)

    def enable(self):
        self._enable.on()

    def disable(self):
        self._enable.off()

    def enableLimiter(self, pin_a=None, pin_b=None, debounce_ms=500):
        if pin_a:
            self._limiter_a = DebouncedInput(pin_a, DebouncedInput.Low, debounce_ms)
            self._limiter_a.callback = self._limiterHandler
        if pin_b:
            self._limiter_b = DebouncedInput(pin_b, DebouncedInput.Low, debounce_ms)
            self._limiter_b.callback = self._limiterHandler

    def disableLimiter(self):
        if self._limiter_a:
            self._limiter_a.disable()
        if self._limiter_b:
            self._limiter_b.disable()

    def _limiterHandler(self, pin=-1):
        if self._limiter_a and self.status == CW and pin == self._limiter_a.pin_num:
            self._pwm_a.duty_u16(0)
        elif self._limiter_b and self.status == CCW and pin == self._limiter_b.pin_num:
            self._pwm_b.duty_u16(0)


class VoltageController(DAC5571):
    MAX_VOLTAGE = const(35.34)
    BITS = const(8)
    VDD = const(3.3)
    OFFSET = const(0.297)

    def __init__(self, i2c):
        super().__init__(i2c)
        self._weight = (pow(2, self.BITS) - 1) / self.VDD - self.OFFSET

    def setVoltage(self, val):
        self.set(self.vol2vdac(val))

    def vol2vdac(self, val):
        # Vout = MAX_VOLTAGE - 9*Vdac
        # Vdac = (MAX_VOLTAGE - Vout) / 9
        val = 24 if val > 24 else val
        val = 6 if val < 6 else val
        vdac = (self.MAX_VOLTAGE - val) / 9
        return round(vdac * self._weight)


class PIDcontroller(PID):
    def __init__(self, motor: Motor):
        super().__init__()
        self.target = 0
        self.lock = False
        self._motor = motor
        self._update_timer = Timer(-1)
        self._interval = 0.1
        self._dt_offset = 0

    def init(self, kp, ki, kd, absMax, scale, mode, period_ms, isAuto=False):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.absMax = absMax
        self.scale = scale
        self.mode = mode
        self._interval = period_ms / 1000
        if isAuto:
            self._update_timer.init(mode=Timer.PERIODIC, period=period_ms, callback=self.callback)

    def callback(self, timer=-1):
        if self.lock is False:
            out = self.update(self._motor.encoder.pos, self.target, self._interval + self._dt_offset)
            speed = round(out * self.scale)
         
            self._motor.setSpeed(speed)
            return out
  
        else:
            self._dt_offset += self._interval
            return 0
