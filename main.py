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
                [sg.Text("n0"), sg.InputText("27", size=20, key='n0'), sg.Text("n1"), sg.InputText("100", size=20,
                                                                                                  key='n1')],
                [sg.Checkbox('Show Euler', default=True, enable_events=True, key='EM2')],
                [sg.Checkbox('Show Improved Euler', default=True, enable_events=True, key='EI2')],
                [sg.Checkbox('Show Runge-Kutta', default=True, enable_events=True, key='ER2')],
                [sg.Button("Count errors"), sg.Button("Close")]]

layout2 = [[sg.Frame('graph', graph2_layout), sg.Frame('menu', menu2_layout)]]

tab2_layout = sg.Tab("Page 2", layout2)

tabGroup = [[sg.TabGroup([[tab1_layout, tab2_layout]])]]

window = sg.Window("best window", tabGroup, finalize=True)

b = GraphErrorCalculator.GraphErrorCalculator(a, 27, 100)

printer = Printer.Printer()

printer.print_1_page_graph(a, window)
printer.print_2_page_graph(b, window)

while True:
    event, values = window.read()
    print(event, values)
    if event == 'Close0' or event == 'Close' or event == sg.WINDOW_CLOSED:
        break
    elif event in ['ES1', 'EM1', 'EI1', 'ER1']:
        printer.print_1_page_graph(a, window, bool(values['ES1']), bool(values['EM1']), bool(values['EI1']), bool(values['ER1']))
    elif event == "Draw and Calculate":
        if float(values['x0']) <= 0 and float(values['x1']) >= 0:
            printer.print_error_1(window, "The interval contains point of discontinuity (x = 0).\n"
                                          "Graph can not be plotted")
        elif int(values['N']) < 2:
            printer.print_error_1(window, "Number of N is too small.\n"
                                          "Graph can not be plotted")
        elif int(values['n0']) < 2:
            printer.print_error_1(window, f"Number of n0 is too small. Recommended at least {int(float(values['x1']) - float(values['x0'])) + 1}.\n"
                                          "Graph can not be plotted for those values")
        else:
            a.resolve(f, float(values['x0']), float(values['y0']), float(values['x1']), int(values['N']))
            printer.print_1_page_graph(a, window, bool(values['ES1']), bool(values['EM1']), bool(values['EI1']), bool(values['ER1']))
            b.newValues(a, int(values['n0']), int(values['n1']))
            printer.print_2_page_graph(b, window, bool(values['EM2']), bool(values['EI2']), bool(values['ER2']))
    elif event in ['EM2', 'EI2', 'ER2']:
        printer.print_2_page_graph(b, window, bool(values['EM2']), bool(values['EI2']), bool(values['ER2']))
    elif event == "Count errors":
        if int(values['n0']) < 2:
            printer.print_error_1(window,
                                  f"Number of n0 is too small. Recommended at least {int(float(values['x1']) - float(values['x0'])) + 1}.\n"
                                  "Graph can not be plotted for those values")
        else:
            b.newValues(a, int(values['n0']), int(values['n1']))
            printer.print_2_page_graph(b, window, bool(values['EM2']), bool(values['EI2']), bool(values['ER2']))
window.close()
