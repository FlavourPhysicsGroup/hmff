r"""实现文章1103.2655中对 $f_{B\pi}$ 形状因子的参数化"""
import fdm
import numpy as np


def z(q2):
    m_B = fdm.parameters_dict['m_B+']
    m_pi = fdm.parameters_dict['m_pi+']
    q2_min = -6          # 这个量是多少? 不清楚.
    t_plus = (m_B + m_pi)**2
    t_0 = t_plus - 2 * np.sqrt(m_B * m_pi) * np.sqrt(t_plus - q2_min)
    term1 = np.sqrt(t_plus - q2)
    term2 = np.sqrt(t_plus - t_0)
    return (term1 - term2) / (term1 + term2)


def f_plus(q2):
    f_0 = 0.281
    b_1 = -1.62
    m2_B = fdm.parameters_dict['m_B*+']**2        # 这个量是多少? 不清楚.
    pre_factor = f_0 / (1 - q2 / m2_B)
    return pre_factor * (1 + b_1 * (z(q2) - z(0)) + (z(q2)**2 - z(0)**2) * b_1 / 2)


def f_0(q2):
    f_0 = 0.281
    b_1 = -3.98
    return f_0 * (1 + b_1 * (z(q2) - z(0)))


def ff(q2):
    return {'f+': f_plus(q2), 'f0': f_0(q2), 'fT': None}
