#!/usr/bin/env python

from math import sqrt

# z parameterization
# see the equation in the note

### z parameter
# dependence: tp, t0, a_0, a_1, a_2, ..., a_N-1
def z(q2, pars):
    tp = pars.get('tp')
    t0 = pars.get('t0')
    return (sqrt(1-q2/tp) - sqrt(1-t0/tp))/ (sqrt(1-q2/tp) + sqrt(1-t0/tp))


# parameterization: BCL_1
# dependence: tp, t0, m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_1(q2, pars):
    z = z(q2, pars) # not checked
    m_star = pars.get('m_star')
    a_list = [value for key, value in pars.items() if key.startswith('a_')] # not checked
    N = len(a_list)
    return sum(
                1/(1-q2/m_star**2) * a * (z**n - (-1)**(n-N)*(n/N)*z**N)
                for n, a in enumerate(a_list)
                )


# parameterization: BCL_2
# dependence: tp, t0, a_0, a_1, a_2, ..., a_N-1
def f_BCL_2(q2, pars):
    z = z(q2, pars) # not checked
    a_list = [value for key, value in pars.items() if key.startswith('a_')] # not checked
    N = len(a_list)
    return sum(
                a * z**n 
                for n, a in enumerate(a_list)
                )


# parameterization: BCL_3
# dependence: tp, t0, m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_3(q2, pars):
    z = z(q2, pars) # not checked
    m_star = pars.get('m_star')
    a_list = [value for key, value in pars.items() if key.startswith('a_')] # not checked
    N = len(a_list)
    return sum(
                1/(1-q2/m_star**2) * a * z**n 
                for n, a in enumerate(a_list)
                )