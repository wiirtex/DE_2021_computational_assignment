from abc import ABCMeta


class ComputationalSolution(metaclass=ABCMeta):
    _computedValues = list()
    _error = list()
    _exactValues = list()
    _interval = float

    def __init__(self, exact_values: list, f, interval):
        self._exactValues = exact_values
        self._f = f
        self._interval = interval

    def solve(self, x0, y):
        pass

    def getComputedValues(self):
        pass

    def getErrors(self):
        pass
