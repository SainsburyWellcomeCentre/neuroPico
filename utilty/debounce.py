from machine import Pin, Timer
from micropython import const


class DebouncedInput(Pin):
    """Micropython Debounced GPIO Input Class"""

    Low = const(0)
    High = const(1)

    def __init__(self, pin_num:int, activate_logic=0, debounce_ms=100):
        super().__init__(pin_num, Pin.IN)
        self.pin_num = pin_num
        self.__db_timer = Timer(-1)
        self.__debounce_ms = debounce_ms
        self.__activate_logic = activate_logic

        self.enable(callback=self.__doNothing)

    def enable(self, callback):
        self.callback = callback
        self.irq(self.__irqHandler, Pin.IRQ_FALLING | Pin.IRQ_RISING)

    def disable(self):
        self.irq(trigger=0)

    def __DebounceTimerExpired(self, timer):
        if self.value() == self.__activate_logic:
            self.callback(self.pin_num)
        self.irq(self.__irqHandler, Pin.IRQ_FALLING | Pin.IRQ_RISING)

    def __irqHandler(self, pin):
        self.__db_timer.init(
            mode=Timer.ONE_SHOT,
            period=self.__debounce_ms,
            callback=self.__DebounceTimerExpired,
        )
        self.irq(trigger=0)

    def __doNothing(self, pin):
        return
