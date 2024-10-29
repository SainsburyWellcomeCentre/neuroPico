from neopixel import NeoPixel
from machine import Pin


class WS2812C(NeoPixel):
    def __init__(self, pin: Pin, isOFF=True, colour=(0, 0, 0)):
        super().__init__(pin, 1)
        self.colour = colour
        self.isOFF = isOFF
        self._update()

    def setColour(self, rgb):
        self.colour = rgb
        self.isOFF = rgb == (0, 0, 0)
        self._update()

    def toggle(self):
        self.isOFF = not (self.isOFF)
        self._update()

    def on(self):
        self.isOFF = False
        self._update()

    def off(self):
        self.isOFF = True
        self._update()

    def _update(self):
        newColour = (0, 0, 0) if self.isOFF else self.colour
        self.fill(newColour)
        self.write()
