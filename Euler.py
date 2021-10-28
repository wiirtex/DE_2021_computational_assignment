from computationalSolution import ComputationalSolution
import math


class EulerSolution(ComputationalSolution):
    def solve(self, x0, y0: float):
        if len(self._x) > 0:
            self._computedValues = [y0]
            self._error = [0]
        for i in range(1, len(self._x)):
            self._computedValues.append(self._computedValues[-1] + self._interval * self._f(self._x[i], self._computedValues[-1]))

            self._error.append(math.fabs(self._exactValues[i] - self._computedValues[-1]))
        # self._error.append(math.fabs(self._exactValues[1] - self._computedValues[-1]))

    def getComputedValues(self):
        return self._computedValues

    def getErrors(self):
        return self._error
