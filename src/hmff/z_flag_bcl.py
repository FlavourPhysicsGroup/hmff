from copy import deepcopy

import numpy as np


def format_parameters_flag_bcl(pars):
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
    marker_keys = {"m_1", "mm_1", "m0_1"}
    matched_markers = marker_keys & keys

    if len(matched_markers) != 1:
        raise ValueError(f"pars 中必须且只能包含 {marker_keys} 中的一个，")

    if {"tp", "t0"} <= keys:
        return pars

    if {"m_1", "m_2"} <= keys:
        m_1 = pars["m_1"]
        m_2 = pars["m_2"]

        pars["tp"] = (m_1 + m_2) ** 2
        pars["t0"] = (m_1 + m_2) * (np.sqrt(m_1) - np.sqrt(m_2)) ** 2
    elif {"mm_1", "mm_2"} <= keys:
        mp_1 = pars["mp_1"]
        mp_2 = pars["mp_2"]
        mm_1 = pars["mm_1"]
        mm_2 = pars["mm_2"]

        tp = (mp_1 + mp_2) ** 2
        tm = (mm_1 - mm_2) ** 2
        pars["tp"] = tp
        pars["t0"] = tp - np.sqrt(tp * (tp - tm))
    elif {"m0_1", "m0_2"} <= keys:
        mp_1 = pars["mp_1"]
        mp_2 = pars["mp_2"]
        m0_1 = pars["m0_1"]
        m0_2 = pars["m0_2"]

        pars["tp"] = (mp_1 + mp_2) ** 2
        pars["t0"] = (m0_1 - m0_2) ** 2
    else:
        raise ValueError(f"Invalid keys in pars: {sorted(keys)}")
    return pars


def get_z(qsq: float, pars: dict) -> float:
    tp = pars["tp"]
    t0 = pars["t0"]

    sqrt_tp_q = np.sqrt(tp - qsq)
    sqrt_tp_t0 = np.sqrt(tp - t0)

    return (sqrt_tp_q - sqrt_tp_t0) / (sqrt_tp_q + sqrt_tp_t0)


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_1(qsq: float, pars: dict) -> float:
    """BCL 参数化公式之一, 参见 FLAG arXiv:2411.04268v1 eq.527, eq.540, eq.544,
    主要用于矢量形状因子 f_+

    Args:
        qsq: 转移动量平方
        pars: 参数化数据

    Returns:
        形状因子参数
    """
    m_star = pars.get("m_star")
    z = get_z(qsq, pars)
    a_array = np.asarray(pars.get("a"))

    N = a_array.size
    n_array = np.arange(N)

    z_series = z**n_array - (-1.0) ** (n_array - N) * (n_array / N) * z**N
    return np.dot(a_array, z_series) / (1.0 - qsq / m_star**2)


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_2(qsq: float, pars: dict) -> float:
    """
    BCL 参数化公式之一, 参见 FLAG arXiv:2411.04268v1 eq.547,
    主要用于矢量形状因子 f_+

    Args:
        qsq: 转移动量平方
        pars: 参数化数据

    Returns:
        形状因子参数
    """
    z = get_z(qsq, pars)  # not checked
    a_array = np.asarray(pars.get("a"))

    N = a_array.size
    n_array = np.arange(N)

    z_series = z**n_array - (-1.0) ** (n_array - N) * (n_array / N) * z**N
    return np.dot(a_array, z_series)


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_3(qsq: float, pars: dict) -> float:
    """
    BCL 参数化公式之一, 参见 FLAG arXiv:2411.04268v1 eq.541,
    主要用于标量形状因子 f_0

    Args:
        qsq: 转移动量平方
        pars: 参数化数据

    Returns:
        形状因子参数
    """
    z = get_z(qsq, pars)  # not checked
    a_array = np.asarray(pars.get("a"))

    n_array = np.arange(a_array.size)

    z_series = z**n_array
    return np.dot(a_array, z_series)


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_4(qsq: float, pars: dict) -> float:
    """
    BCL 参数化公式之一, 参见 FLAG arXiv:2411.04268v1 eq.545,
    主要用于标量形状因子 f_0

    Args:
        qsq: 转移动量平方
        pars: 参数化数据

    Returns:
        形状因子参数
    """
    z = get_z(qsq, pars)  # not checked
    m_star = pars.get("m_star")
    a_array = np.asarray(pars.get("a"))

    n_array = np.arange(a_array.size)

    z_series = z**n_array
    return np.dot(a_array, z_series) / (1.0 - qsq / m_star**2)


def a0_last_prepare(f0_info: dict, fp_info: dict) -> dict:
    """根据 f0(q^2=0) = f+(q^2=0) 约束，计算 f0 的末位系数 a_{N-1},
    并写入 f0_config["parameter"]["a"]。

    Args:
        f0_config: 形状因子 f0 的所有参数信息, YAML 中的多行数据
        fp_config: 形状因子 fp 的所有参数信息, YAML 中的多行数据

    Raises:
        ValueError:
        KeyError:

    Returns:
        f0_config: 更新后的 f0_config，末位系数 a_{N-1} 已写入
    """
    f0_config = deepcopy(f0_info)
    fp_config = deepcopy(fp_info)
    ret_pars = deepcopy(f0_config["parameter"])
    _METCH_METHOD = {"BCL 1": f_BCL_1, "BCL 2": f_BCL_2, "BCL 3": f_BCL_3, "BCL 4": f_BCL_4}
    if f0_config.get("a0_last") == "by_ap":
        f0_func = _METCH_METHOD[f0_config["parameterization"]]
        fp_func = _METCH_METHOD[fp_config["parameterization"]]
        f0_pars = format_parameters_flag_bcl(f0_config["parameter"])
        fp_pars = format_parameters_flag_bcl(fp_config["parameter"])

        a0_list = f0_pars["a"]
        a0_list_auxiliary = [0] * (len(a0_list) + 1)
        a0_list_auxiliary[-1] = 1

        pars_0_auxiliary = deepcopy(f0_pars)
        pars_0_auxiliary["a"] = a0_list_auxiliary
        f0_0 = f0_func(0.0, f0_pars)
        fp_0 = fp_func(0.0, fp_pars)
        f0_last_term = f0_func(0.0, pars_0_auxiliary)

        a0_last = (fp_0 - f0_0) / f0_last_term

        ret_pars["a"].append(float(a0_last))
        return ret_pars
    else:
        raise ValueError(
            f"Invalid value for a0_last: {f0_config.get('a0_last')}. Expected 'by_ap'."
        )


# ---------------------------------------------------------------------------
# 形状因子误差计算（解析梯度 + 协方差传播）
# ---------------------------------------------------------------------------
# 四个 f_BCL 函数对 a 参数都是线性的，因此解析梯度就是对应的基函数。
# 协方差矩阵由 Impl.__build_covariance_matrix 在初始化时构造（YAML 中直接
# 给出 covariance_matrix，或由 correlation_matrix 与各形状因子 error 字段
# 的 1 sigma 误差构造：Cov_ij = rho_ij * sigma_i * sigma_j），存入
# config["covariance_matrix"]["value"]（两者都未给出时为标量 0）。
# 误差传播：sigma_f^2(q^2) = g^T . Cov . g，g 为对全部拟合参数的梯度。


def errors(qsq: float, config: dict) -> dict:
    """计算 impl 内所有形状因子在指定 q^2 处的 1 sigma 误差

    全局参数空间 = 按形状因子出现顺序拼接各 error["a"]（仅含独立拟合参数，
    与协方差矩阵的次序一致）。局部梯度通过零填充嵌入全局向量后再与全局
    协方差矩阵做二次型。末位系数由 a0_last 约束导出的形状因子（f0，其
    len(a) = len(error["a"]) + 1，末位已由 Impl.__prepare__ 算好并附加在
    a 末尾）用 gradient_a0_last 求梯度，此时 f+ 参数块也有非零分量。

    Args:
        qsq: 转移动量平方（只接受标量；需要向量化时请用 np.vectorize 封装）
        config: impl 的全部配置信息（Impl.config，a0_last 与协方差矩阵已算好）

    Returns:
        dict，{ff_name: 1 sigma 误差 (float)}
    """

    def df_da_BCL(qsq, pars, class_func):
        """形状因子对其自身 a 参数的解析梯度（局部梯度）

        BCL 1/2 的基函数为 (z^n - (-1)^(n-N) (n/N) z^N)，BCL 3/4 的基函数为 (z^n)；
        BCL 1/4 再乘极点因子 1/(1 - q^2/m_star^2)。

        Args:
            qsq: 转移动量平方（标量）
            pars: 经 format_parameters_flag_bcl 格式化后的参数
            class_func: 参数化名称，"BCL 1" / "BCL 2" / "BCL 3" / "BCL 4" 之一

        Returns:
            np.ndarray，长度等于 len(pars["a"])
        """
        a_array = np.asarray(pars["a"], dtype=float)
        N = a_array.size
        n_array = np.arange(N)
        z = get_z(qsq, pars)

        if class_func in ("BCL 1", "BCL 2"):
            grad = z**n_array - (-1.0) ** (n_array - N) * (n_array / N) * z**N
        elif class_func in ("BCL 3", "BCL 4"):
            grad = z**n_array
        else:
            raise ValueError(f"Invalid class_func: {class_func}. 期望 'BCL 1'-'BCL 4' 之一。")

        if class_func in ("BCL 1", "BCL 4"):
            m_star = pars["m_star"]
            grad = grad / (1.0 - qsq / m_star**2)
        return np.asarray(grad, dtype=float)

    def gradient_a0_last(qsq, pars_f0, class_func_f0, pars_fp, class_func_fp):
        """带 a0_last 约束（f_+(0) = f_0(0)）的 f0 对全局参数的解析梯度

        Args:
            qsq: 转移动量平方（标量）
            pars_f0: f0 格式化后的参数（a 为 YAML 中列出的、不含末位约束系数）
            class_func_f0: f0 的参数化名称（"BCL 3" 或 "BCL 4"）
            pars_fp: f+ 格式化后的参数
            class_func_fp: f+ 的参数化名称（如 "BCL 1"）

        Returns:
            np.ndarray，长度 len(a_f+) + len(a_f0)，次序为 f+ 在前、f0 在后
        """
        a_f0 = np.asarray(pars_f0["a"], dtype=float)
        M = a_f0.size + 1  # f0 实际系数个数（含约束导出的末位系数）

        z = get_z(qsq, pars_f0)
        z0 = get_z(0.0, pars_f0)

        # f0 的极点因子（BCL 3 无极点，q^2=0 处极点因子恒为 1）
        if class_func_f0 == "BCL 4":
            m_star = pars_f0["m_star"]
            pole = 1.0 / (1.0 - qsq / m_star**2)
        else:
            pole = 1.0

        # f+ 在 q^2=0 处的局部梯度（基函数），即 d f_+(0) / d a_k(f+)
        grad_fp_at_0 = df_da_BCL(0.0, pars_fp, class_func_fp)

        factor = pole * z ** (M - 1) / z0 ** (M - 1)
        grad = np.concatenate(
            [
                factor * grad_fp_at_0,
                pole
                * (z ** np.arange(M - 1) - z0 ** np.arange(M - 1) / z0 ** (M - 1) * z ** (M - 1)),
            ]
        )
        return np.asarray(grad, dtype=float)

    ff_configs = config["form factors"]
    cov = config["covariance_matrix"]["value"]
    if np.ndim(cov) == 0:
        # Impl 未提供协方差/关联矩阵（哨兵值 0），误差视为 0
        return {name: 0.0 for name in ff_configs}
    dim = cov.shape[0]

    # 全局参数次序 = 形状因子出现顺序，每个形状因子内部按 a 下标
    offsets = {}
    pos = 0
    for name, ff_cfg in ff_configs.items():
        offsets[name] = pos
        pos += len(ff_cfg["error"]["a"])
    if pos != dim:
        raise ValueError(f"独立参数总数 ({pos}) 与协方差矩阵维度 ({dim}) 不一致。")

    result = {}
    for name, ff_cfg in ff_configs.items():
        pars = format_parameters_flag_bcl(ff_cfg["parameter"])
        n_indep = len(ff_cfg["error"]["a"])
        g = np.zeros(dim)
        if len(pars["a"]) == n_indep:
            # 无约束：局部梯度直接填入该形状因子的参数块
            g[offsets[name] : offsets[name] + n_indep] = df_da_BCL(
                qsq, pars, ff_cfg["parameterization"]
            )
        else:
            # a0_last 约束：独立参数为 a[:-1]，梯度横跨 f+ 与 f0 两块
            fp_cfg = ff_configs["f+"]
            pars_fp = format_parameters_flag_bcl(fp_cfg["parameter"])
            pars_trim = {**pars, "a": pars["a"][:-1]}
            pair = gradient_a0_last(
                qsq, pars_trim, ff_cfg["parameterization"], pars_fp, fp_cfg["parameterization"]
            )
            n_fp = len(pars_fp["a"])
            g[offsets["f+"] : offsets["f+"] + n_fp] = pair[:n_fp]
            g[offsets[name] : offsets[name] + n_indep] = pair[n_fp:]
        result[name] = float(np.sqrt(g @ cov @ g))
    return result