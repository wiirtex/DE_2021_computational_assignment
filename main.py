from copy import copy

import diffEquation
import Function
import PySimpleGUI as sg
import numpy as np
import Printer
import GraphErrorCalculator

f = Function.Variant1()
a = diffEquation.DifferentialEquation(f, 1, 2, 10, 9)

sg.theme("DarkAmber")

graph1_layout = [[sg.Canvas(key='pyplot1_figure')]]

menu1_layout = [[sg.Text("My work:")],
                [sg.Text("x0"), sg.InputText("1", size=20, key='x0'), sg.Text("y0"),
                 sg.InputText("2", size=20, key='y0')],
                [sg.Text("x1"), sg.InputText("10", size=20, key='x1'), sg.Text("N"),
                 sg.InputText("9", size=20, key='N')],
                [sg.Checkbox('Show Exact', default=True, enable_events=True, key='ES1')],
                [sg.Checkbox('Show Euler', default=True, enable_events=True, key='EM1')],
                [sg.Checkbox('Show Improved Euler', default=True, enable_events=True, key='EI1')],
                [sg.Checkbox('Show Runge-Kutta', default=True, enable_events=True, key='ER1')],
                [sg.Button("Draw and Calculate"), sg.Button("Close")]]

layout1 = [[sg.Frame('graph', graph1_layout), sg.Frame('menu', menu1_layout)]]

tab1_layout = sg.Tab("Page 1", layout1)

graph2_layout = [[sg.Canvas(key='pyplot2_figure')]]

menu2_layout = [[sg.Text("My work:")],
                [sg.Text("n0"), sg.InputText("9", size=20, key='n0'), sg.Text("n1"), sg.InputText("100", size=20,
                                                                                                  key='n1')],
                [sg.Checkbox('Show Euler', default=True, enable_events=True, key='EM2')],
                [sg.Checkbox('Show Improved Euler', default=True, enable_events=True, key='EI2')],
                [sg.Checkbox('Show Runge-Kutta', default=True, enable_events=True, key='ER2')],
                [sg.Button("Count errors"), sg.Button("Close")]]

layout2 = [[sg.Frame('graph', graph2_layout), sg.Frame('menu', menu2_layout)]]

tab2_layout = sg.Tab("Page 2", layout2)

tabGroup = [[sg.TabGroup([[tab1_layout, tab2_layout]])]]

window = sg.Window("best window", tabGroup, finalize=True)

b = GraphErrorCalculator.GraphErrorCalculator(a, 9, 100)

printer = Printer.Printer()

printer.print_1_page_graph(a, window)
printer.print_2_page_graph(b, window)

while True:
    event, values = window.read()
    print(event, values)
    if event == 'Close0' or event == 'Close' or event == sg.WINDOW_CLOSED:
        break
    elif event in [4, 5, 6, 7]:
        printer.print_1_page_graph(a, window, bool(values[4]), bool(values[5]), bool(values[6]), bool(values[7]))
    elif event == "Draw and Calculate":
        a.resolve(f, float(values['x0']), float(values['y0']), float(values['x1']), int(values['N']))
        printer.print_1_page_graph(a, window, bool(values['ES1']), bool(values['EM1']), bool(values['EI1']), bool(values['ER1']))
        b.newValues(a, int(values['n0']), int(values['n1']))
        printer.print_2_page_graph(b, window, bool(values['EM2']), bool(values['EI2']), bool(values['ER2']))
    elif event in [10, 11, 12]:
        printer.print_2_page_graph(b, window, bool(values['EM2']), bool(values['EI2']), bool(values['ER2']))
    elif event == "Count errors":
        b.newValues(a, int(values['n0']), int(values['n1']))
        printer.print_2_page_graph(b, window, bool(values['EM2']), bool(values['EI2']), bool(values['ER2']))
window.close()

# class Printer:
#     def print(self, number_of_subplots: int, list_of_plots: list):
#         fig, axs = plt.subplots(number_of_subplots, 3, sharex="all")
#         for i in range(3):
#             for k in range(number_of_subplots):
#                 for j in range(len(list_of_plots[i][k]) - 1):
#                     print(i)
#                     axs[k][i].plot(list_of_plots[i][k][j].x, list_of_plots[i][k][j].y, list_of_plots[i][k][j].color)
#                 axs[k][i].set_title(list_of_plots[i][k][-1])
#
#         fig.suptitle("Plots:")
#         fig.tight_layout()
#         draw(window['pyplot_figure'].TKCanvas, fig)
#         # plt.show()
#
#
# class SolverAndDrawer:
#     printer = Printer()
#     graphs = list()
#     eulerSolver: EulerSolver
#     improvedSolver: ImprovedEulerSolver
#     rungeSolver: RungeKuttaSolver
#     x0: float
#     y0: float
#     x1: float
#     interval: float
#     eAns = dict()
#     iAns = dict()
#     rAns = dict()
#
#     def __init__(self, x0: float, y0: float, x1: float, interval: float):
#         self.x0 = x0
#         self.x1 = x1
#         self.y0 = y0
#         self.interval = interval
#         self.eulerSolver = EulerSolver(x0, y0)
#         self.improvedSolver = ImprovedEulerSolver(x0, y0)
#         self.rungeSolver = RungeKuttaSolver(x0, y0)
#
#     def create_dict(self, dictionary: dict, ans: tuple):
#         dictionary["x"] = ans[4]
#         dictionary["calculated"] = ans[0]
#         dictionary["exact"] = ans[1]
#         dictionary["localError"] = ans[2]
#         dictionary["globalError"] = ans[3]
#
#     def solve_all(self):
#         self.create_dict(self.eAns, self.eulerSolver.solve(self.x1, self.interval))
#         self.create_dict(self.iAns, self.improvedSolver.solve(self.x1, self.interval))
#         self.create_dict(self.rAns, self.rungeSolver.solve(self.x1, self.interval))
#
#     def print(self):
#         self.printer.print(2, [[[Graph(self.eAns["x"], self.eAns["calculated"], "r"),
#                                 Graph(self.eAns["x"], self.eAns["exact"], "b"),
#                                 "Calculated and Exact:"],
#                                [Graph(self.eAns["x"], self.eAns["localError"], "c"),
#                                 Graph(self.eAns["x"], self.eAns["globalError"], "m"),
#                                 "Local and Global Errors:"]],
#                                [[Graph(self.iAns["x"], self.iAns["calculated"], "r"),
#                                 Graph(self.iAns["x"], self.iAns["exact"], "b"),
#                                 "Calculated and Exact:"],
#                                 [Graph(self.iAns["x"], self.iAns["localError"], "c"),
#                                  Graph(self.iAns["x"], self.iAns["globalError"], "m"),
#                                  "Local and Global Errors:"]],
#                                [[Graph(self.rAns["x"], self.rAns["calculated"], "r"),
#                                 Graph(self.rAns["x"], self.rAns["exact"], "b"),
#                                 "Calculated and Exact:"],
#                                 [Graph(self.rAns["x"], self.rAns["localError"], "c"),
#                                  Graph(self.rAns["x"], self.rAns["globalError"], "m"),
#                                  "Local and Global Errors:"]],
#                                ],)
#
# #
# #
# def draw(canvas, figure):
#     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#     return figure_canvas_agg
#
