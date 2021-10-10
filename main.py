import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Function:
    c: float

    def solve_ivp(self, x: float, y: float):
        self.c = (y + x) / x ** 2

    @staticmethod
    def get_derivative(x: float, y: float) -> float:
        return 1 + 2 * y / x

    def get_exact(self, x: float) -> float:
        return self.c * x * x - x


class ISolver:
    localError: list
    globalError: list
    exact: list
    calculated: list
    x: list
    f: Function
    x0: float
    y0: float

    def __init__(self, x0: float, y0: float):
        self.x0 = x0
        self.y0 = y0
        self.f = Function()
        self.f.solve_ivp(x0, y0)

    def solve(self, end: float, interval: float) -> (list, list, list, list, list):
        pass


class EulerSolver(ISolver):
    def __init__(self, x0: float, y0: float):
        super().__init__(x0, y0)

    def solve(self, end: float, interval: float) -> (list, list, list, list, list):
        self.calculated = [self.y0]
        self.exact = [self.y0]
        xi = self.x0
        self.x = [self.x0]
        self.localError = [0]
        self.globalError = [0]
        while xi <= end:
            self.calculated.append(self.calculated[-1] + interval * self.f.get_derivative(xi, self.calculated[-1]))
            xi += interval
            self.x.append(xi)
            self.exact.append(self.f.get_exact(xi))
            self.globalError.append(self.exact[-1] - self.calculated[-1])
            self.localError.append(self.exact[-1] - self.exact[-2] - interval * self.f.get_derivative(xi - interval,
                                                                                                      self.exact[-2]))
        return self.calculated, self.exact, self.localError, self.globalError, self.x


class ImprovedEulerSolver(ISolver):
    def __init__(self, x0: float, y0: float):
        super().__init__(x0, y0)

    def solve(self, end: float, interval: float) -> (list, list, list, list, list):
        self.calculated = [self.y0]
        self.exact = [self.y0]
        xi = self.x0
        self.x = [self.x0]
        self.localError = [0]
        self.globalError = [0]
        while xi <= end:
            self.calculated.append(self.calculated[-1] + interval * self.f.get_derivative(
                xi + interval / 2, self.calculated[-1] + interval / 2 * self.f.get_derivative(xi, self.calculated[-1])))
            xi += interval
            self.x.append(xi)
            self.exact.append(self.f.get_exact(xi))
            self.globalError.append(self.exact[-1] - self.calculated[-1])
            self.localError.append(self.exact[-1] - self.exact[-2] - interval * self.f.get_derivative(
                xi - interval / 2, self.calculated[-2] + interval / 2 * self.f.get_derivative(
                    xi - interval, self.calculated[-2])))

        return self.calculated, self.exact, self.localError, self.globalError, self.x


class RungeKuttaSolver(ISolver):
    def __init__(self, x0: float, y0: float):
        super().__init__(x0, y0)

    def solve(self, end: float, interval: float) -> (list, list, list, list, list):
        self.calculated = [self.y0]
        self.exact = [self.y0]
        xi = self.x0
        self.x = [self.x0]
        self.localError = [0]
        self.globalError = [0]
        while xi <= end:
            k1 = self.f.get_derivative(xi, self.calculated[-1])
            k2 = self.f.get_derivative(xi + interval / 2, self.calculated[-1] + interval * k1 / 2)
            k3 = self.f.get_derivative(xi + interval / 2, self.calculated[-1] + interval * k2 / 2)
            k4 = self.f.get_derivative(xi + interval, self.calculated[-1] + interval * k3)

            self.calculated.append(self.calculated[-1] + interval / 6 * (k1 + 2 * k2 + 2 * k3 + k4))
            xi += interval
            self.x.append(xi)
            self.exact.append(self.f.get_exact(xi))
            self.globalError.append(self.exact[-1] - self.calculated[-1])
            k1 = self.f.get_derivative(xi - interval, self.calculated[-2])
            k2 = self.f.get_derivative(xi - interval / 2, self.calculated[-2] + interval * k1 / 2)
            k3 = self.f.get_derivative(xi - interval / 2, self.calculated[-2] + interval * k2 / 2)
            k4 = self.f.get_derivative(xi, self.calculated[-2] + interval * k3)
            prev = k1, k2, k3, k4
            self.localError.append(
                self.exact[-1] - self.exact[-2] - interval / 6 * (prev[0] + 2 * prev[1] + 2 * prev[2] + prev[3]))

        return self.calculated, self.exact, self.localError, self.globalError, self.x


class Graph:
    x: list
    y: list
    color = "c"

    def __init__(self, x_: list, y_: list, str_: str = None):
        self.x = x_
        self.y = y_
        if str_ is not None:
            self.color = str_


class Printer:
    def print(self, number_of_subplots: int, list_of_plots: list):
        fig, axs = plt.subplots(number_of_subplots, 3, sharex="all")
        for i in range(3):
            for k in range(number_of_subplots):
                for j in range(len(list_of_plots[i][k]) - 1):
                    print(i)
                    axs[k][i].plot(list_of_plots[i][k][j].x, list_of_plots[i][k][j].y, list_of_plots[i][k][j].color)
                axs[k][i].set_title(list_of_plots[i][k][-1])

        fig.suptitle("Plots:")
        fig.tight_layout()
        draw(window['pyplot_figure'].TKCanvas, fig)
        # plt.show()


class SolverAndDrawer:
    printer = Printer()
    graphs = list()
    eulerSolver: EulerSolver
    improvedSolver: ImprovedEulerSolver
    rungeSolver: RungeKuttaSolver
    x0: float
    y0: float
    x1: float
    interval: float
    eAns = dict()
    iAns = dict()
    rAns = dict()

    def __init__(self, x0: float, y0: float, x1: float, interval: float):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.interval = interval
        self.eulerSolver = EulerSolver(x0, y0)
        self.improvedSolver = ImprovedEulerSolver(x0, y0)
        self.rungeSolver = RungeKuttaSolver(x0, y0)

    def create_dict(self, dictionary: dict, ans: tuple):
        dictionary["x"] = ans[4]
        dictionary["calculated"] = ans[0]
        dictionary["exact"] = ans[1]
        dictionary["localError"] = ans[2]
        dictionary["globalError"] = ans[3]

    def solve_all(self):
        self.create_dict(self.eAns, self.eulerSolver.solve(self.x1, self.interval))
        self.create_dict(self.iAns, self.improvedSolver.solve(self.x1, self.interval))
        self.create_dict(self.rAns, self.rungeSolver.solve(self.x1, self.interval))

    def print(self):
        self.printer.print(2, [[[Graph(self.eAns["x"], self.eAns["calculated"], "r"),
                                Graph(self.eAns["x"], self.eAns["exact"], "b"),
                                "Calculated and Exact:"],
                               [Graph(self.eAns["x"], self.eAns["localError"], "c"),
                                Graph(self.eAns["x"], self.eAns["globalError"], "m"),
                                "Local and Global Errors:"]],
                               [[Graph(self.iAns["x"], self.iAns["calculated"], "r"),
                                Graph(self.iAns["x"], self.iAns["exact"], "b"),
                                "Calculated and Exact:"],
                                [Graph(self.iAns["x"], self.iAns["localError"], "c"),
                                 Graph(self.iAns["x"], self.iAns["globalError"], "m"),
                                 "Local and Global Errors:"]],
                               [[Graph(self.rAns["x"], self.rAns["calculated"], "r"),
                                Graph(self.rAns["x"], self.rAns["exact"], "b"),
                                "Calculated and Exact:"],
                                [Graph(self.rAns["x"], self.rAns["localError"], "c"),
                                 Graph(self.rAns["x"], self.rAns["globalError"], "m"),
                                 "Local and Global Errors:"]],
                               ],)

# x0 = 1.
# b = 3
# y0 = 2.
# h = 0.1
#
# eulerSolver = EulerSolver(x0,y0)
# improverSolver = ImprovedEulerSolver(x0, y0)
# rungeSolver = RungeKuttaSolver(x0, y0)
#
# yi, ye, lte, gte = eulerSolver.solve(x0, y0, b, h)
# x = list(np.arange(x0, b + h/2, h))
# graph1 = Graph(x, yi)
# graph2 = Graph(x, ye)
#
# printer = Printer()
# printer.add_graph(graph1)
# printer.add_graph(graph2)
# printer.print()
#
# print(yi, ye, lte, gte, sep='\n')

def draw(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

sg.theme("DarkAmber")

tab1_layout = [[sg.Canvas(key='pyplot_figure')]]

menu_layout = [[sg.Text("My work:")],
          [sg.Text("x0"), sg.InputText("1", size=20), sg.Text("y0"), sg.InputText("2", size=20)],
          [sg.Text("x1"), sg.InputText("10", size=20), sg.Text("interval"), sg.InputText("0.1", size=20)],
          [sg.Button("Draw and Calculate"), sg.Button("Close")]]

layout = [[sg.Frame('a', tab1_layout), sg.Frame('b', menu_layout)]]



window = sg.Window("best window", layout)



while True:
    event, values = window.read()
    print(event, values)
    if event == 'Close' or event == sg.WINDOW_CLOSED:
        break
    elif event == "Draw and Calculate":
        solverAndDrawer = SolverAndDrawer(float(values[0]), float(values[1]), float(values[2]), float(values[3]))
        solverAndDrawer.solve_all()
        solverAndDrawer.print()
window.close()
