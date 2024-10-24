import time
from machine import Pin, Timer, PWM
from motor import Motor

class PID:
    
    # Instance variable for this class
    posPrev = 0

    # Constructor for initializing PID values
    def __init__(self, kp:float=1, ki:float=0, kd:float=0, max:float=0.8):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max  = max
        self.eprev = 0
        self.eintegral = 0
        self.target = 0

    # Function for calculating the Feedback signal. It takes the current value, user target value and the time delta.
    def evalu(self, value, target, deltaT):
        
        # Propotional
        e = target-value 

        # Derivative
        dedt = (e-self.eprev)/(deltaT)

        # Integral
        self.eintegral = self.eintegral + e*deltaT
        
        # Control signal
        u = self.kp*e + self.kd*dedt + self.ki*self.eintegral
        
        if u > self.max:
            u = self.max
        elif u < -self.max:
            u = -self.max

        self.eprev = e
        return u
    
    # Function for closed loop position control
    def setTarget(self, pos, target, deltaT):
    
        # Control signal call
        result = self.evalu(pos, target, deltaT)
        # Set the speed 
        if abs(result) < 0.05:
            return 0
        else:
            return result

myMotor = Motor(6,7,23,20000,4,5)
myMotor.enable()
myMotor.enableEncoder()

p = PID(0.5, 0, 0, 0.2)
tt = 0
ctime = time.ticks_us()
def printPos(timer):
    global ctime, tt
    tdiff = time.ticks_diff(time.ticks_us(), ctime)
    res = p.setTarget(myMotor.getPos()/361, tt/361, tdiff/1_000_000)
    myMotor.setSpeed(res*65535)
    print(myMotor.getPos(), tt, tt-myMotor.getPos())
    ctime = time.ticks_us()

myTimer = Timer()
myTimer.init(freq=40, mode=Timer.PERIODIC, callback=printPos)

while True:
    tt = myMotor.getPos() + 240
    time.sleep_ms(1500)


# from driver.as5600 import AS5600

# dev = NeuroPico()


# def callbackBTN(pin):
#     if pin == NeuroPico.PIN_BTNA:
#         print("A")
#     elif pin == NeuroPico.PIN_BTNB:
#         print("B")


# dev.BTNA.callback = callbackBTN
# dev.BTNB.callback = callbackBTN

# led = dev.LED

# led.setColour((100, 100, 100))

# while True:
#     led.toggle()
#     time.sleep_ms(500)


#     from machine import Pin, Timer, PWM, ADC
# import time


# led_G = Pin(22, Pin.OUT, value=0)
# led_R = Pin(21, Pin.OUT, value=1)
# led_B = Pin(25, Pin.OUT, value=1)


# #
# from micropython import const

# #

# # from machine import SoftI2C
# # i2c = SoftI2C(scl=23, sda=24, freq=100000)  # create software I2C object

# # i2c.writeto(76, b'123')
# # i2c.readfrom(76, 4)

# from neuropico import NeuroPico

# p=NeuroPico()


# vr = ADC(Pin(26))

# ADC_timer = Timer()
# LED_timer = Timer()
# VR_timer = Timer()

# flag = False


# def switchLED(timer):
#     global led_B
#     led_B.on()


# THLD = 5000

# knob = 0


# def log2linear(x):

#     a = 1.2e-14
#     b = -1.5e-9
#     c = 6.4e-5

#     y = a * x**3 + b * x**2 + c * x
#     return y


# def tick(timer):
#     global flag, ir_A
#     if ir_A.threshold - ir_A.value() > THLD:
#         flag = True


# def vrr(timer):
#     global knob, ir_A
#     knob = log2linear(vr.read_u16())
#     ir_A.brightness(round(knob * 65500))


# ADC_timer.init(freq=1000, mode=Timer.PERIODIC, callback=tick)

# VR_timer.init(freq=10, mode=Timer.PERIODIC, callback=vrr)


# while True:
#     if flag:
#         led_B.off()
#         LED_timer.init(period=1500, mode=Timer.ONE_SHOT, callback=switchLED)
#         flag = False

#     print(ir_A.value(), end="\t")
#     print(knob, end="\t\n")
#     # print(ir_A.value())
#     time.sleep_ms(10)
