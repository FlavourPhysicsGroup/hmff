#!/usr/bin/env python

from math import sqrt

# z parameterization
# see the equation in the note

### determine the cases of key
# keys_case_1: {mp_1, mp_2, mm_1, mm_2}
# keys_case_2: { m_1,  m_2}
# keys_case_3: {mp_1, mp_2, m0_1, m0_2}
#      other: e.g., {mm_1, mm_2, mp_1, mp_2, m_1, m_2} or {}
def get_key_case(pars):
    # 定义键集合和对应的case编号
    mass_cases = {
        frozenset({'mp_1', 'mp_2', 'mm_1', 'mm_2'}): 1,
        frozenset({ 'm_1',  'm_2'}): 2,
        frozenset({'mp_1', 'mp_2', 'm0_1', 'm0_2'}): 3
    }
    
    # pars包含的所有的key
    pars_keys = frozenset(pars.keys())

    # return the case number of the mass keys if pars contain any mass key belonging to that case
    # e.g., pars = {'mm_1': 1, 'm_1': 5} -> return [1,2]
    matching_any_mass = []
    for key_set, case_num in mass_cases.items():
        if key_set.intersection(pars_keys):
            matching_any_mass.append(case_num)

    ### step 1: consistency check
    # e.g., pars = {'a': 1} -> raise ValueError
    if len(matching_any_mass) == 0:
        raise ValueError("Invalid parameter keys: Neither {mm_1, mm_2, mp_1, mp_2}, {m_1, m_2} or {m0_1, m0_2} are found in YAML.")
    # e.g., pars = {'mm_1': 1, 'm_1': 5, 'm_2': 6} -> raise ValueError
    elif len(matching_any_mass) > 1:
        raise ValueError("Invalid parameter keys: expected either {mm_1, mm_2, mp_1, mp_2}, {m_1, m_2} or {m0_1, m0_2} exclusively.")

    ### step 2: return the case number
    for key_set, case_num in mass_cases.items():
        if case_num in matching_any_mass and key_set.issubset(pars_keys):
            return case_num

    ### step 3: raise error if not complete mass keys
    raise ValueError("Invalid parameter keys: expected either {mm_1, mm_2, mp_1, mp_2}, {m_1, m_2} or {m0_1, m0_2}.")


### get mm_1, mm_2, mp_1, mp_2 from pars
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


### t0 parameter by using definition 1
def get_t0_1(pars):
    tp = get_tp(pars)
    tm = get_tm(pars)
    return tp-sqrt(tp*(tp-tm))

### t0 parameter by using definition 2
def get_t0_2(pars):
    m0_1 = pars.get('m0_1')
    m0_2 = pars.get('m0_2')
    return (m0_1 - m0_2)**2

### t0 parameter
def get_t0(pars):
    key_case = get_key_case(pars)
    # if use mp_1, mp_2, m0_1, m0_2
    if key_case == 3:
        return get_t0_2(pars)
    # if use {mp_1, mp_2, mm_1, mm_2} or {m_1, m_2}
    else :
        return get_t0_1(pars)


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
    a_list = pars.get('a')
    N = len(a_list)
    return sum(
                1/(1-q2/m_star**2) * a * (z**n - (-1)**(n-N)*(n/N)*z**N)
                for n, a in enumerate(a_list)
                )


# parameterization: BCL_2
# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_2(q2, pars):
    z = get_z(q2, pars) # not checked
    a_list = pars.get('a')
    N = len(a_list)
    return sum(
                a * (z**n - (-1)**(n-N)*(n/N)*z**N)
                for n, a in enumerate(a_list)
                )


# parameterization: BCL_3
# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_3(q2, pars):
    z = get_z(q2, pars) # not checked
    a_list = pars.get('a')
    N = len(a_list)
    return sum(
                a * z**n 
                for n, a in enumerate(a_list)
                )


# parameterization: BCL_4
# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_4(q2, pars):
    z = get_z(q2, pars) # not checked
    m_star = pars.get('m_star')
    a_list = pars.get('a')
    N = len(a_list)
    return sum(
                1/(1-q2/m_star**2) * a * z**n 
                for n, a in enumerate(a_list)
                )


### function to get a0_N-1 from ap
# This function is used to get a0_N-1 from ap by using the relation f_p(0) = f_0(0)
# depending on both pars_p and pars_0
# When the keys satisfy the following conditions:
# 1. 'by_ap' contained in f0.a, e.g., f0:a:[0.561, 0.65955, by_ap]
# 2. f+.parameterization = 'BCL 1'
# 3. f0.parameterization = 'BCL 2' or 'BCL 3'
# the main program should call this function to update f0.a by replacing 'by-ap' with the value of this function returns.
def get_a0_N_minus_1_from_ap(pars_p, pars_0):
    z0 = get_z(0.0, pars_0)
    N = len(pars_p.get('a'))     # N is the number of ap in the parameterization
    fp_0 = f_BCL_1(0.0, pars_p)  # f_p(0)
    a0_list = pars_0.get('a')    # a0_1, a0_2, ..., a0_N-1
    return (fp_0-sum(a * z0**n for n, a in enumerate(a0_list[:-1])))*z0**(1-N)

def f_z_expansions_1(q2, pars):
    raise NotImplementedError

def f_z_expansions_2(q2, pars):
    raise NotImplementedError

def f_z_expansions_3(q2, pars):
    raise NotImplementedError