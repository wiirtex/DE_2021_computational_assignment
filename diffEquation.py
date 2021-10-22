import math

from methods import computationalSolution as cs
import Function
from methods import Euler
from methods import Improved
from methods import RungeKutta


class DifferentialEquation:

    def __init__(self, f: Function.AbstractFunction, x0: float, y0: float, x: float, n: int):
        self.__x0 = x0
        self.__y0 = y0
        self.__X = x
        self.__x = list()
        self.__exactValues = list()
        self.__n = n
        self.__function = f

        self.__ivp = f.solve_ivp
        self.__ivp(self.__x0, self.__y0)
        self.__Y = f.get_exact
        self.__interval = 1 / self.__n * (self.__X - self.__x0)
        self.__countX()
        self.__countExactValues()
        self.__f = f.get_derivative

        self.__solve()

    def resolve(self, f: Function.AbstractFunction, x0: float, y0: float, x: float, n: int):
        self.__init__(f, x0, y0, x, n)

    def resolve_n(self, n: int):
        self.__init__(self.__function, self.__x0, self.__y0, self.__X, n)

    def __solve(self):
        self.__euler = Euler.EulerSolution(self.getExactValues(), self.__f, self.__interval)
        self.__improved = Improved.ImprovedSolution(self.getExactValues(), self.__f, self.__interval)
        self.__runge = RungeKutta.RungeKuttaSolution(self.getExactValues(), self.__f, self.__interval)
        self.__euler.solve(self.__x0, self.__y0)
        self.__improved.solve(self.__x0, self.__y0)
        self.__runge.solve(self.__x0, self.__y0)

    def getConstant(self):
        return self.__ivp(self.__x0, self.__y0)

    def getCalculatedValues(self):
        return self.__euler.getComputedValues(), self.__improved.getComputedValues(), self.__runge.getComputedValues()

    def getErrors(self):
        return self.__euler.getErrors(), self.__improved.getErrors(), self.__runge.getErrors()

    def __countX(self):
        self.__x.clear()
        for i in range(self.__n):
            self.__x.append(self.__x0 + i * self.__interval)

    def getXValues(self) -> list:
        if len(self.__x) == 0:
            self.__countX()
        return self.__x

    def __countExactValues(self):
        self.__countX()
        self.__exactValues.clear()
        for i in range(len(self.__x)):
            self.__exactValues.append(self.__Y(self.__x[i]))

    def getExactValues(self) -> list:
        if len(self.__exactValues) != len(self.__x):
            self.__countExactValues()
        return self.__exactValues
