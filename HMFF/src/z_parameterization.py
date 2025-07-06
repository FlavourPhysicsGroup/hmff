#!/usr/bin/env python

from math import sqrt

# z parameterization
# see the equation in the note

### determine the cases of key
# keys_case_1: {mm_1, mm_2, mp_1, mp_2}
# keys_case_2: { m_1, m_2}
#      other: e.g., {mm_1, mm_2, mp_1, mp_2, m_1, m_2} or {}
def get_key_case(pars):
    keys_case_1 = {'mm_1', 'mm_2', 'mp_1', 'mp_2'}
    keys_case_2 = {'m_1', 'm_2'}
    has_case_1_keys = all(k in pars for k in keys_case_1)
    has_case_2_keys = all(k in pars for k in keys_case_2)
    if has_case_1_keys and not has_case_2_keys:       # keys_case_1: {mm_1, mm_2, mp_1, mp_2}
        return 1
    elif has_case_2_keys and not has_case_1_keys:     # keys_case_2: {m_1, m_2}
        return 2
    elif not has_case_1_keys and not has_case_2_keys: # e.g., {}
        raise ValueError("Invalid parameter keys: Neither {'mm_1', 'mm_2', 'mp_1', 'mp_2'} or {'m_1', 'm_2'} are found in YAML.")
    else:                                             # e.g., {mm_1, m_1}
        raise ValueError("Invalid parameter keys: expected either {'mm_1', 'mm_2', 'mp_1', 'mp_2'} or {'m_1', 'm_2'} exclusively.")


# mass_name: mm_1, mm_2, mp_1, mp_2
def get_mass(mass_name, pars):
    key_case = get_key_case(pars)
    if key_case == 1:
        return pars.get(mass_name)
    elif key_case == 2:
        # mass_name is like 'mm_1', 'mm_2', 'mp_1', 'mp_2'
        # Remove the second character ('m' or 'p'), e.g., 'mm_1' -> 'm_1', 'mp_2' -> 'm_2'
        return pars.get(mass_name[0] + mass_name[2:])


### tp parameter
def get_tp(pars):
    mp_1 = get_mass('mp_1', pars)
    mp_2 = get_mass('mp_2', pars)
    return (mp_1 + mp_2)**2


### tm parameter
def get_tm(pars):
    mm_1 = get_mass('mm_1', pars)
    mm_2 = get_mass('mm_2', pars)
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
