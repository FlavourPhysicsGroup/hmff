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
    f0 = pars["f(0)"]
    c = pars["c"]
    P = pars["P"]
    term = (z - z0) * (1 + (z + z0) / 2)
    f = (f0 + c * term) / (1 - P * qsq)
    return f


def f_etmc_2(qsq, pars):
    z = get_z(qsq, pars)
    z0 = get_z(0, pars)
    f0 = pars["f(0)"]
    c = pars["c"]
    Ms = pars["m_star"]
    term = (z - z0) * (1 + (z + z0) / 2)
    f = (f0 + c * term) / (1 - qsq / Ms**2)
    return f


def f_etmc_3(qsq, pars):
    z = get_z(qsq, pars)
    z0 = get_z(0, pars)
    f0 = pars["f(0)"]
    c = pars["c"]
    term = (z - z0) * (1 + (z + z0) / 2)
    f = f0 + c * term
    return f


def errors(qsq: float, config: dict) -> dict:
    """计算形状因子误差. 
    参数误差以协方差矩阵给出, 见 config["covariance_matrix"]["value"]

    Args:
        qsq: 转移动量平方(只接受标量；需要向量化时请用 np.vectorize 封装)
        config: impl 的全部配置信息（Impl.config，a0_last 与协方差矩阵已算好）

    Returns:
       dict，{ff_name: 1 sigma 误差 (float)}
    """

    def local_gradient(ff_cfg: dict) -> dict:
        """单个形状因子对其拟合参数的解析梯度

        三种参数化共享基函数项 term = (z - z0) * (1 + (z + z0) / 2):
        ETMC 1: f = (f(0) + c * term) / (1 - P * q^2)，对 f(0)、c、P 求导
        ETMC 2: f = (f(0) + c * term) / (1 - q^2 / m_star^2)，m_star 为固定
                常数（不在协方差矩阵中），仅对 f(0)、c 求导
        ETMC 3: f = f(0) + c * term，仅对 f(0)、c 求导

        Args:
            ff_cfg: 单个形状因子的配置（含 parameterization 与 parameter）

        Returns:
            dict，{参数种类 ("f(0)" / "c" / "P"): 导数值}
        """
        pars = format_parameters(ff_cfg["parameter"])
        z = get_z(qsq, pars)
        z0 = get_z(0.0, pars)
        term = (z - z0) * (1 + (z + z0) / 2)
        f0 = pars["f(0)"]
        c = pars["c"]

        parameterization = ff_cfg["parameterization"]
        if parameterization == "ETMC 1":
            denom = 1.0 - pars["P"] * qsq
            return {
                "f(0)": 1.0 / denom,
                "c": term / denom,
                "P": qsq * (f0 + c * term) / denom**2,
            }
        if parameterization == "ETMC 2":
            denom = 1.0 - qsq / pars["m_star"] ** 2
            return {"f(0)": 1.0 / denom, "c": term / denom}
        if parameterization == "ETMC 3":
            return {"f(0)": 1.0, "c": term}
        raise ValueError(f"Invalid parameterization: {parameterization}")

    ff_configs = config["form factors"]
    cov = config["covariance_matrix"]["value"]
    if np.ndim(cov) == 0:
        # Impl 未提供协方差矩阵（哨兵值 0），误差视为 0
        return {name: 0.0 for name in ff_configs}

    # 全局参数次序由 covariance_matrix.order 给出，
    # 形如 [f(0), c_f0, c_f+, P_f0, P_f+]（f(0) 为各形状因子共享参数）
    order = config["covariance_matrix"]["order"]
    index = {param_name: i for i, param_name in enumerate(order)}
    dim = len(order)

    result = {}
    for name, ff_cfg in ff_configs.items():
        g = np.zeros(dim)
        for kind, value in local_gradient(ff_cfg).items():
            key = kind if kind == "f(0)" else f"{kind}_{name}"
            g[index[key]] = value
        result[name] = float(np.sqrt(g @ cov @ g))
    return result

