#!/usr/bin/env python

# pole-dominance parameterization
# see the equation in the note


# parameterization name: one pole
def f_one_pole(q2, pars):
    a = pars.get('a')
    msq = pars.get('m') ** 2
    return a / (1 - q2 / msq)

# parameterization name: double pole 1
def f_double_pole_1(q2, pars):
    a1 = pars.get('a1')
    a2 = pars.get('a2')
    m1sq = pars.get('m1') ** 2
    m2sq = pars.get('m2') ** 2
    return a1 / (1 - q2 / m1sq) + a2 / (1 - q2 / m2sq)

# parameterization name: double pole 2
def f_double_pole_2(q2, pars):
    a1 = pars.get('a1')
    a2 = pars.get('a2')
    msq = pars.get('m') ** 2
    return a1 / (1 - q2 / msq) + a2 / (1 - q2 / msq) ** 2
