#!/usr/bin/env python

from math import sqrt

# z parameterization
# see the equation in the note

### determine the cases of key
# key_case_1: {mm_1, mm_2, mp_1, mp_2}
# key_case_2: { m_1, m_2}
#      other: e.g., {mm_1, mm_2, mp_1, mp_2, m_1, m_2}
def get_key_case(pars):
    keys_case_1 = {'mm_1', 'mm_2', 'mp_1', 'mp_2'}
    keys_case_2 = {'m_1', 'm_2'}
    if all(k in pars for k in keys_case_1) and not any(k in pars for k in keys_case_2):
        return 1  # key_case_1: {mm_1, mm_2, mp_1, mp_2}
    elif all(k in pars for k in keys_case_2) and not any(k in pars for k in keys_case_1):
        return 2  # key_case_2: {m_1, m_2}
    else:
        raise ValueError("Invalid parameter keys: expected either {'mm_1', 'mm_2', 'mp_1', 'mp_2'} or {'m_1', 'm_2'} exclusively.")


### tp parameter
def get_tp(pars):
    key_case = get_key_case(pars)
    if key_case == 1:
        mp_1 = pars.get('mp_1')
        mp_2 = pars.get('mp_2')
    elif key_case == 2:
        mp_1 = pars.get('m_1')
        mp_2 = pars.get('m_2')
    return (mp_1 + mp_2)**2


### tm parameter
def get_tm(pars):
    key_case = get_key_case(pars)
    if key_case == 1:
        mm_1 = pars.get('mm_1')
        mm_2 = pars.get('mm_2')
    elif key_case == 2:
        mm_1 = pars.get('m_1')
        mm_2 = pars.get('m_2')
    return (mm_1 - mm_2)**2


### t0 parameter
def get_t0(pars):
    tp = get_tp(pars)
    tm = get_tm(pars)
    return tp-sqrt(tp*(tp-tm))


### z parameter
def get_z(q2, pars):
    tp = get_tp(pars)
    t0 = get_t0(pars)
    return (sqrt(1-q2/tp) - sqrt(1-t0/tp))/ (sqrt(1-q2/tp) + sqrt(1-t0/tp))


# parameterization: BCL_1
# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_1(q2, pars):
    z = get_z(q2, pars) # not checked
    m_star = pars.get('m_star')
    a_list = [value for key, value in pars.items() if key.startswith('a_')] # not checked
    N = len(a_list)
    return sum(
                1/(1-q2/m_star**2) * a * (z**n - (-1)**(n-N)*(n/N)*z**N)
                for n, a in enumerate(a_list)
                )


# parameterization: BCL_2
# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_2(q2, pars):
    z = get_z(q2, pars) # not checked
    a_list = [value for key, value in pars.items() if key.startswith('a_')] # not checked
    N = len(a_list)
    return sum(
                a * z**n 
                for n, a in enumerate(a_list)
                )


# parameterization: BCL_3
# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_3(q2, pars):
    z = get_z(q2, pars) # not checked
    m_star = pars.get('m_star')
    a_list = [value for key, value in pars.items() if key.startswith('a_')] # not checked
    N = len(a_list)
    return sum(
                1/(1-q2/m_star**2) * a * z**n 
                for n, a in enumerate(a_list)
                )
