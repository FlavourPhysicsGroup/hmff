import sys

#!/usr/bin/env python

# pole-dominance parameterization
# see the equation in the note

### get mass squared from parameters
# this function is needed, since pars could contain either 'mass' or 'mass_sq',
# mass_name: m, m1, m2
def get_mass_sq(mass_name, pars):
    mass_sq_key = f"{mass_name}_sq"
    has_mass_sq = mass_sq_key in pars
    has_mass = mass_name in pars
    if has_mass_sq and not has_mass:     # e.g., pars = {'m_sq': 1.0}
        return pars[mass_sq_key]
    elif not has_mass_sq and has_mass:   # e.g., pars = {'m': 1.0}
        return pars[mass_name] ** 2
    elif has_mass_sq and has_mass:       # e.g., pars = {'m_sq': 1.0, 'm': 1.0}
        raise ValueError(f"Both '{mass_sq_key}' and '{mass_name}' are present in YAML.")
    else:                                                 # e.g., pars = {}
        raise ValueError(f"Neither '{mass_sq_key}' nor '{mass_name}' found in YAML.")


# parameterization: one pole
# pars: {a, m(_sq)}
def f_one_pole(q2, pars):
    a = pars.get('a')
    m_sq = get_mass_sq('m', pars)
    return a / (1 - q2 / m_sq)


# parameterization: double pole 1
# pars: {a1, a2, m1(_sq), m2(_sq)}
def f_double_pole_1(q2, pars):
    a1 = pars.get('a1')
    a2 = pars.get('a2')
    m1_sq = get_mass_sq('m1', pars)
    m2_sq = get_mass_sq('m2', pars)
    return a1 / (1 - q2 / m1_sq) + a2 / (1 - q2 / m2_sq)


# parameterization: double pole 2
# pars: {a1, a2, m(_sq)}
def f_double_pole_2(q2, pars):
    a1 = pars.get('a1')
    a2 = pars.get('a2')
    m_sq = get_mass_sq('m', pars)
    return a1 / (1 - q2 / m_sq) + a2 / (1 - q2 / m_sq) ** 2
