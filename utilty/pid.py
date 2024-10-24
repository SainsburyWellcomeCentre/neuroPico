class PID:
    
    # Instance variable for this class
    posPrev = 0

    # Constructor for initializing PID values
    def __init__(self, kp:float=1, ki:float=0, kd:float=0, max:float=0.8):
        self.kp = kp
        self.kd = kd
        self.ki = ki
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
        else:
            u = u 
        self.eprev = e
        return u
    
    # Function for closed loop position control
    def setTarget(self, pos, target, deltaT):
    
        # Control signal call
        result = int(self.evalu(pos, target, deltaT))
        # Set the speed 
        if abs(result) < 5:
            return 0
        else:
            return result
