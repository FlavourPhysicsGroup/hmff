from inspect import _void
from multiprocessing import Value
import sys

#!/usr/bin/env python

# pole-dominance parameterization
# see the equation in the note




### format the parameters
# pars from YAML -> standard pars

# one_pole
# pars: {a, m(_sq)} -> {a, m_sq}
def format_parameters_one_pole(pars):
    if pars.keys() == {'a', 'm_sq'}:
        return
    elif pars.keys() == {'a', 'm'}:
        pars['m_sq'] = pars['m'] ** 2
        del pars['m']
        return
    elif {'m', 'm_sq'}.issubset(pars.keys()):
        raise ValueError("Invalid parameter keys: expected either 'm_sq' or 'm'.")
    elif not {'a'}.issubset(pars.keys()):
        raise ValueError("Invalid parameter keys: expected 'a'.")
    else:
        raise ValueError("Invalid parameter keys: expected {a, m_sq} or {a, m}.")

# double_pole_1
# pars: {a1, a2, m1(_sq), m2(_sq)} -> {a1, a2, m1_sq, m2_sq}
def format_parameters_double_pole_1(pars):
    if pars.keys() == {'a1', 'a2', 'm1_sq', 'm2_sq'}:
        return 
    elif pars.keys() == {'a1', 'a2', 'm1', 'm2'}:
        pars['m1_sq'] = pars['m1'] ** 2
        pars['m2_sq'] = pars['m2'] ** 2
        del pars['m1']
        del pars['m2']
        return
    elif pars.keys() == {'a1', 'a2', 'm1', 'm2_sq'}:
        pars['m1_sq'] = pars['m1'] ** 2
        del pars['m2_sq']
        return
    elif pars.keys() == {'a1', 'a2', 'm1_sq', 'm2'}:
        pars['m2_sq'] = pars['m2'] ** 2
        del pars['m2']
        return
    elif {'m1', 'm1_sq'}.issubset(pars.keys()) or {'m2', 'm2_sq'}.issubset(pars.keys()):
        raise ValueError("Invalid parameter keys: expected either 'm1' or 'm1_sq' and either 'm2' or 'm2_sq'.")
    elif not {'a1', 'a2'}.issubset(pars.keys()):
        raise ValueError("Invalid parameter keys: expected 'a1' and 'a2'.")
    else:
        raise ValueError("Invalid parameter keys: expected {a1, a2, m1_sq, m2_sq} or {a1, a2, m1, m2}.")

# double_pole_2
# pars: {a1, a2, m(_sq)} -> {a1, a2, m_sq}
def format_parameters_double_pole_2(pars):
    if pars.keys() == {'a1', 'a2', 'm_sq'}:
        return
    elif pars.keys() == {'a1', 'a2', 'm'}:
        pars['m_sq'] = pars['m'] ** 2
        del pars['m']
        return
    elif {'m', 'm_sq'}.issubset(pars.keys()):
        raise ValueError("Invalid parameter keys: expected either 'm_sq' or 'm'.")
    elif not {'a1', 'a2'}.issubset(pars.keys()):
        raise ValueError("Invalid parameter keys: expected 'a1' and 'a2'.")
    else:
        raise ValueError("Invalid parameter keys: expected {a1, a2, m_sq} or {a1, a2, m}.")




### parameterization function

# one pole
# standard pars: {a, m_sq}
def f_one_pole(q2, pars):
    a = pars.get('a')
    m_sq = pars.get('m_sq')
    return a / (1 - q2 / m_sq)


# double pole 1
# standard pars: {a1, a2, m1_sq, m2_sq}
def f_double_pole_1(q2, pars):
    a1 = pars.get('a1')
    a2 = pars.get('a2')
    m1_sq = pars.get('m1_sq')
    m2_sq = pars.get('m2_sq')
    return a1 / (1 - q2 / m1_sq) + a2 / (1 - q2 / m2_sq)


# parameterization: double pole 2
# standard pars: {a1, a2, m_sq}
def f_double_pole_2(q2, pars):
    a1 = pars.get('a1')
    a2 = pars.get('a2')
    m_sq = pars.get('m_sq')
    return a1 / (1 - q2 / m_sq) + a2 / (1 - q2 / m_sq) ** 2
