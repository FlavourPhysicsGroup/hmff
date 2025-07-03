#!/usr/bin/env python

# pole-dominance parameterization
# see the equation in the note


# parameterization name: one pole
# pars: {a, m_sq}
def f_one_pole(q2, pars):
    a = pars.get('a')
    m_sq = pars.get('m_sq')
    return a / (1 - q2 / m_sq)

# parameterization name: double pole 1
# pars: {a1, a2, m1_sq, m2_sq}
def f_double_pole_1(q2, pars):
    a1 = pars.get('a1')
    a2 = pars.get('a2')
    m1_sq = pars.get('m1_sq')
    m2_sq = pars.get('m2_sq')
    return a1 / (1 - q2 / m1_sq) + a2 / (1 - q2 / m2_sq)

# parameterization name: double pole 2
# pars: {a1, a2, m_sq}
def f_double_pole_2(q2, pars):
    a1 = pars.get('a1')
    a2 = pars.get('a2')
    m_sq = pars.get('m_sq')
    return a1 / (1 - q2 / m_sq) + a2 / (1 - q2 / m_sq) ** 2
