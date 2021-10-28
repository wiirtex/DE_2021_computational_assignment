import Manager
import diffEquation
import Function

f = Function.Variant1()
a = diffEquation.DifferentialEquation(f, 1, 2, 10, 20)

manager = Manager.Manager(a, f)

manager.run()
