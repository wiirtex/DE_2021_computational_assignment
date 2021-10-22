import math
from copy import copy, deepcopy

import diffEquation


class GraphErrorCalculator:

    def __init__(self, eq: diffEquation.DifferentialEquation, n0: int, nlast: int):
        self.errors = [list(), list(), list()]
        self.n0 = n0
        self.n1 = nlast
        self.equation = deepcopy(eq)
        self.valuesChanged = True

    def newValues(self, eq: diffEquation.DifferentialEquation, n0: int, nlast: int):
        self.n0 = n0
        self.n1 = nlast
        self.equation = deepcopy(eq)
        self.valuesChanged = True

    def getConstant(self):
        return self.equation.getConstant()

    def getXValues(self) -> list:
        self.X = list()
        for i in range(self.n1 - self.n0):
            self.X.append(i + self.n0)
        return self.X

    def getMaxError(self) -> list:
        if not self.valuesChanged:
            return self.errors
        self.errors = [list(), list(), list()]
        for i in range(self.n1 - self.n0):
            self.equation.resolve_n(self.n0 + i)
            errors = self.equation.getErrors()
            self.errors[0].append(max(errors[0]))
            self.errors[1].append(max(errors[1]))
            self.errors[2].append(max(errors[2]))
        self.valuesChanged = False
        return self.errors
