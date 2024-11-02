from machine import Pin


class Encoder:

    def __init__(self, pin_a, pin_b):
        self._encoder_a = Pin(pin_a, Pin.IN)
        self._encoder_b = Pin(pin_b, Pin.IN)
        self.pos = 0
        self.lock = False

    def enable(self):
        self._encoder_b.irq(self._irqHandler, Pin.IRQ_RISING)

    def disable(self):
        self._encoder_b.irq(trigger=0)

    def reset(self):
        self.lock = True
        self.pos = 0
        self.lock = False

    def _irqHandler(self, pin=-1):
        # TODO: add edge condition
        # 0	1 0	0 -1
        # 0	1 1 0 -2  (assume pin1 edges only)
        # 1	1 0 0 +2  (assume pin1 edges only)
        # 1	1 1 0 +1

        if self.lock is False:
            if self._encoder_a.value() == 1:
                self.pos += 1
            else:
                self.pos -= 1
