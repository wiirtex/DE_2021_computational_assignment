import diffEquation

import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from GraphErrorCalculator import GraphErrorCalculator


class Printer:
    i: FigureCanvasTkAgg = None
    j: FigureCanvasTkAgg = None

    def print_1_page_graph(self, eq: diffEquation.DifferentialEquation, window: sg.Window, showExact=True,
                           showEuler=True, showImproved=True,
                           showRunge=True):
        x = eq.getXValues()
        ex = eq.getExactValues()
        errors = eq.getErrors()
        values = eq.getCalculatedValues()
        fig, axs = plt.subplots(2, sharex="all")

        if showExact:
            axs[0].plot(x, ex, label="Exact Values", color="magenta")
        if showEuler:
            axs[0].plot(x, values[0], label="Euler Method", color="tab:orange")
            axs[1].plot(x, errors[0], label="Euler Method Error", color="tab:orange")
        if showImproved:
            axs[0].plot(x, values[1], label="Improved Method", color="tab:green")
            axs[1].plot(x, errors[1], label="Improved Method Error", color="tab:green")
        if showRunge:
            axs[0].plot(x, values[2], label="Runge-Kutta Method", color="tab:cyan")
            axs[1].plot(x, errors[2], label="Runge-Kutta Method Error", color="tab:cyan")
        fig.tight_layout()
        fig.subplots_adjust(top=0.8)
        fig.suptitle(r"ODE: $1 + \frac{2y}{x}$" + "\n" + r"General Solution: $cx^2-x$" + "\n" + r"Exact Solution: "
                     + f"${eq.getConstant()}x^2-x$")
        axs[0].legend(loc="best")
        axs[1].legend(loc="best")
        figure_canvas_agg = FigureCanvasTkAgg(fig, window['pyplot1_figure'].TKCanvas)
        figure_canvas_agg.get_tk_widget().forget()
        if self.i is not None:
            self.i.get_tk_widget().forget()
        self.i = self.draw(window['pyplot1_figure'].TKCanvas, fig)

    def print_2_page_graph(self, ec: GraphErrorCalculator, window: sg.Window,
                           showEuler=True, showImproved=True, showRunge=True):
        x = ec.getXValues()
        values = ec.getMaxError()

        fig = plt.figure()

        if showEuler:
            plt.plot(x, values[0], label="Euler Method Errors", color="tab:orange")
        if showImproved:
            plt.plot(x, values[1], label="Improved Method Errors", color="tab:green")
        if showRunge:
            plt.plot(x, values[2], label="Runge-Kutta Method Errors", color="tab:cyan")

        plt.legend(loc="best")
        fig.tight_layout()
        fig.subplots_adjust(top=0.8)
        fig.suptitle(r"ODE: $1 + \frac{2y}{x}$" + "\n" + r"General Solution: $cx^2-x$" + "\n" + r"Exact Solution: "
                     + f"${ec.getConstant()}x^2-x$")
        figure_canvas_agg = FigureCanvasTkAgg(fig, window['pyplot2_figure'].TKCanvas)
        figure_canvas_agg.get_tk_widget().forget()
        if self.j is not None:
            self.j.get_tk_widget().forget()
        self.j = self.draw(window['pyplot2_figure'].TKCanvas, fig)

    def draw(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.get_tk_widget()
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg
