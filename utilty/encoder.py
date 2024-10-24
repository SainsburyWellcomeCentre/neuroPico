from machine import Pin

class Encoder:

    def __init__(self, pin_a, pin_b):
        self.__encoder_a = Pin(pin_a, Pin.IN)
        self.__encoder_b = Pin(pin_b, Pin.IN)
        self.pos = 0

    def enable(self):
        self.__encoder_b.irq(self.__irqHandler, Pin.IRQ_RISING)

    def disable(self):
        self.__encoder_b.irq(trigger=0)

    def __irqHandler(self, pin):
        if self.__encoder_a.value() == 1:
            self.pos += 1
        else:
            self.pos -= 1
