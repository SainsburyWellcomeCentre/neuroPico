from machine import Pin, Timer
from micropython import const


class DebouncedInput(Pin):
    """Micropython Debounced GPIO Input Class"""

    Low = const(0)
    High = const(1)

    def __init__(self, pin_num: int, activate_logic=0, debounce_ms=50):
        
        pull = Pin.PULL_DOWN if activate_logic else Pin.PULL_UP
        super().__init__(pin_num, Pin.IN, pull)
        self.pin_num = pin_num
        self._db_timer = Timer(-1)
        self._debounce_ms = debounce_ms
        self._activate_logic = activate_logic
        self._trigger_logic = Pin.IRQ_RISING if activate_logic else Pin.IRQ_FALLING
        self.enable(callback=self._doNothing)

    def enable(self, callback):
        self.callback = callback
        self.irq(self._irqHandler, self._trigger_logic)

    def disable(self):
        self.irq(trigger=0)

    def _DebounceTimerExpired(self, timer):
        if self.value() == self._activate_logic:
            self.callback(self.pin_num)
        self.irq(self._irqHandler, self._trigger_logic)

    def _irqHandler(self, pin=-1):
        self._db_timer.init(
            mode=Timer.ONE_SHOT,
            period=self._debounce_ms,
            callback=self._DebounceTimerExpired,
        )
        self.irq(trigger=0)

    def _doNothing(self, pin=-1):
        return
