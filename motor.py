from machine import Pin
from micropython import const
from utilty.encoder import Encoder
from utilty.debounce import DebouncedInput
from driver.m2619s import M2619S

CW = const(0)
CCW = const(1)
STOP = const(2)

class Motor(M2619S):
    def __init__(
        self,
        pwm_pin_a,
        pwm_pin_b,
        enable_pin,
        pwm_freq=20_000,
        encoder_pin_a=None,
        encoder_pin_b=None
    ):
        super().__init__(pwm_pin_a, pwm_pin_b, pwm_freq)

        if encoder_pin_a and encoder_pin_b:
            self.__encoder = Encoder(encoder_pin_a, encoder_pin_b)
        else:
            self.__encoder = None

        self.__enable = Pin(enable_pin, Pin.OUT, value=0)
        self.status = STOP
        self.__limiter_a = None
        self.__limiter_b = None

    def setSpeed(self, speed):
        direction = CW if speed > 0 else CCW

        if self.__limiter_a and direction == CW and self.__limiter_a.value == 0:
            self.set(0)
            self.status = STOP
        elif self.__limiter_b and direction == CCW and self.__limiter_b.value == 0:
            self.set(0)
            self.status = STOP
        elif speed:
            self.set(speed)
            self.status = direction
        else:
            self.set(speed)
            self.status = STOP

    def enable(self):
        self.__enable.on()

    def disable(self):
        self.__enable.off()

    def enableEncoder(self):
        if self.__encoder:
            self.__encoder.enable()

    def disableEncoder(self):
        if self.__encoder:
            self.__encoder.disable()

    def getPos(self):
        if self.__encoder:
            return self.__encoder.pos
        else:
            return 0

    def enableLimiter(self, pin_a=None, pin_b=None, debounce_ms=500):
        if pin_a:
            self.__limiter_a = DebouncedInput(pin_a, DebouncedInput.Low, debounce_ms)
            self.__limiter_a.callback=self.__limiterHandler
        if pin_b:
            self.__limiter_b = DebouncedInput(pin_b, DebouncedInput.Low, debounce_ms)
            self.__limiter_b.callback=self.__limiterHandler

    def disableLimiter(self):
        if self.__limiter_a:
            self.__limiter_a.disable()
        if self.__limiter_b:
            self.__limiter_b.disable()

    def __limiterHandler(self, pin):
        if self.__limiter_a and self.status == CW and pin == self.__limiter_a.pin_num:
            self.__pwm_a.duty_u16(0)
        elif self.__limiter_b and self.status == CCW and pin == self.__limiter_b.pin_num:
            self.__pwm_b.duty_u16(0)



