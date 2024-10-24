from machine import Pin, PWM

class M2619S:
    def __init__(
        self,
        pwm_pin_a,
        pwm_pin_b,
        pwm_freq=20_000,
    ):
        self.__pwm_a = PWM(Pin(pwm_pin_a), freq=pwm_freq, duty_u16=0)
        self.__pwm_b = PWM(Pin(pwm_pin_b), freq=pwm_freq, duty_u16=0)
        self.speed = 0

    def set(self, speed):
        speed = round(speed)
        speed = 65535 if speed > 65535 else speed
        speed = -65535 if speed < -65535 else speed

        if speed == 0:
            self.__pwm_b.duty_u16(0)
            self.__pwm_a.duty_u16(0)
        elif speed > 0:
            self.__pwm_a.duty_u16(0)
            self.__pwm_b.duty_u16(speed)
        else:
            self.__pwm_b.duty_u16(0)
            self.__pwm_a.duty_u16(-1*speed)

        self.speed = speed
