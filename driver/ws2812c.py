from neopixel import NeoPixel
from machine import Pin

class WS2812C(NeoPixel):
    def __init__(self, pin: Pin, isOFF=True, colour=(0, 0, 0)):
        super().__init__(pin, 1)
        self.colour = colour
        self.isOFF = isOFF
        self.__update()

    def setColour(self, rgb):
        self.colour = rgb
        self.isOFF = rgb == (0, 0, 0)
        self.__update()

    def toggle(self):
        self.isOFF = not (self.isOFF)
        self.__update()

    def on(self):
        self.isOFF = False
        self.__update()

    def off(self):
        self.isOFF = True
        self.__update()

    def __update(self):
        newColour = (0, 0, 0) if self.isOFF else self.colour
        self.fill(newColour)
        self.write()


