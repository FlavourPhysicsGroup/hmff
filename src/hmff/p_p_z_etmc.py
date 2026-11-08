import numpy as np


def format_parameters(pars):
    """根据质量信息, 得到 t_+, t_0 两个中间参数, 将其写入 pars.

    Args:
        pars(dict): 单个形状因子的参数化数据

    Raises:
        ValueError: 给出的YAML原始数据中只能有一种t_0的数据约定

    Returns:
        pars(dict): 字典中新增 t_+, t_0
    """
    pars = dict(pars)
    keys = pars.keys()

    if {"tp", "t0"} <= keys:
        return pars

    if {"m_1", "m_2"} <= keys:
        m_1 = pars["m_1"]
        m_2 = pars["m_2"]

        pars["tp"] = (m_1 + m_2) ** 2
        pars["t0"] = (m_1 + m_2) * (np.sqrt(m_1) - np.sqrt(m_2)) ** 2
    else:
        raise ValueError(f"Invalid keys in pars: {sorted(keys)}")
    return pars


def get_z(qsq: float, pars: dict) -> float:
    tp = pars["tp"]
    t0 = pars["t0"]

    sqrt_tp_q = np.sqrt(tp - qsq)
    sqrt_tp_t0 = np.sqrt(tp - t0)

    return (sqrt_tp_q - sqrt_tp_t0) / (sqrt_tp_q + sqrt_tp_t0)


def f_etmc_1(qsq, pars):
    z = get_z(qsq, pars)
    z0 = get_z(0, pars)
    f0 = pars.get("f(0)")
    c = pars.get("c")
    P = pars.get("P")
    term = (z - z0) * (1 + (z + z0) / 2)
    f = (f0 + c * term) / (1 - P * qsq)
    return f


def f_etmc_2(qsq, pars):
    z = get_z(qsq, pars)
    z0 = get_z(0, pars)
    f0 = pars.get("f(0)")
    c = pars.get("c")
    Ms = pars.get("m_star")
    term = (z - z0) * (1 + (z + z0) / 2)
    f = (f0 + c * term) / (1 - qsq / Ms**2)
    return f


def f_etmc_3(qsq, pars):
    z = get_z(qsq, pars)
    z0 = get_z(0, pars)
    f0 = pars.get("f(0)")
    c = pars.get("c")
    term = (z - z0) * (1 + (z + z0) / 2)
    f = f0 + c * term
    return f
