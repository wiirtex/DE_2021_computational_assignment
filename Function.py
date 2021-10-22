from abc import ABCMeta
import numpy as np


class AbstractFunction(metaclass=ABCMeta):
    c: float

    def solve_ivp(self, x: float, y: float):
        """

        :rtype: object
        """
        pass

    @staticmethod
    def get_derivative(x: float, y: float) -> float:
        pass

    def get_exact(self, x: float) -> float:
        pass


class Variant1(AbstractFunction):
    def solve_ivp(self, x: float, y: float):
        self.c = (y + x) / x ** 2
        return self.c

    @staticmethod
    def get_derivative(x: float, y: float) -> float:
        return 1 + 2 * y / x

    def get_exact(self, x: float) -> float:
        return self.c * x * x - x
