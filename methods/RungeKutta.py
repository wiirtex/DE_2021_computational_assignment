from methods.computationalSolution import ComputationalSolution
import math


class RungeKuttaSolution(ComputationalSolution):
    def solve(self, x0, y0: float):
        self._computedValues = [y0]
        self._error = [0]
        for i in range(1, len(self._x)):
            k1 = self._f(self._x[i], self._computedValues[-1])
            k2 = self._f(self._x[i] + self._interval / 2, self._computedValues[-1] + self._interval * k1 / 2)
            k3 = self._f(self._x[i] + self._interval / 2, self._computedValues[-1] + self._interval * k2 / 2)
            k4 = self._f(self._x[i] + self._interval, self._computedValues[-1] + self._interval * k3)

            self._computedValues.append(self._computedValues[-1] + self._interval / 6 * (k1 + 2 * k2 + 2 * k3 + k4))

            self._error.append(math.fabs(self._exactValues[i - 1] - self._computedValues[-2]))

    def getComputedValues(self):
        return self._computedValues

    def getErrors(self):
        return self._error
