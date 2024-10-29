from micropython import const


class PID:

    POE = const(0)
    POM = const(1)

    # Constructor for initializing PID values
    def __init__(self, kp: float = 1, ki: float = 0, kd: float = 0, absMax: float = 0.8, mode=1):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.absMax = absMax
        self.mode = mode
        self._lastInput = None
        self._lastError = None
        self._proportional = 0
        self._integral = 0

    # Function for calculating the Feedback signal. It takes the current value, user target value and the time delta.
    def update(self, inputVal, target, dt):

        error = target - inputVal

        self._lastInput = inputVal if self._lastInput is None else self._lastInput
        self._lastError = error if self._lastError is None else self._lastError

        dInput = inputVal - self._lastInput
        dError = error - self._lastError

        if self.mode == self.POE:
            self._proportional = self.kp * error
        else:
            self._proportional -= self.kp * dInput

        self._integral += self.ki * error * dt
        self._integral = self._clamp(self._integral)

        if self.mode == self.POE:
            derivative = self.kd * dError / dt
        else:
            derivative = -self.kd * dInput / dt

        # Compute final output
        output = self._proportional + self._integral + derivative
        output = self._clamp(output)

        self._lastInput = inputVal
        self._lastError = error

        return output

    def _clamp(self, val):
        if val > self.absMax:
            return self.absMax
        elif val < -self.absMax:
            return -self.absMax
        else:
            return val
