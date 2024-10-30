from neopixel import NeoPixel
from machine import Pin


class WS2812C(NeoPixel):
    def __init__(self, pin: Pin, isOff=True, colour=(0, 0, 0)):
        super().__init__(pin, 1)
        self.colour = colour
        self.isOff = isOff
        self._update()

    def setColour(self, rgb):
        self.colour = rgb
        self.isOFF = rgb == (0, 0, 0)

    def toggle(self):
        self.isOff = not (self.isOff)
        self._update()

    def on(self):
        self.isOff = False
        self._update()

    def off(self):
        self.isOff = True
        self._update()

    def _update(self):
        newColour = (0, 0, 0) if self.isOff else self.colour
        self.fill(newColour)
        self.write()
