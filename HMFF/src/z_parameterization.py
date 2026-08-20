from numpy import sqrt
from copy import deepcopy
import numpy as np

# z parameterization
# see the equation in the note

### check format of the parameters

# key format of BCL
# m_star is optional
KEY_FORMAT_BCL = [
    {"a", "m_star", "m_1", "m_2", "cov_matrices"},
    {"a", "m_star", "m_1", "m_2"},
    {"a", "m_star", "mp_1", "mp_2", "mm_1", "mm_2", "cov_matrices"},
    {"a", "m_star", "mp_1", "mp_2", "mm_1", "mm_2"}, 
    {"a", "m_star", "mp_1", "mp_2", "m0_1", "m0_2", "cov_matrices"},
    {"a", "m_star", "mp_1", "mp_2", "m0_1", "m0_2"},

]

KEY_FORMAT_BCL_WITHOUT_M_STAR = [
    {"a", "m_1", "m_2", "cov_matrices"},
    {"a", "m_1", "m_2"},
    {"a", "mp_1", "mp_2", "mm_1", "mm_2", "cov_matrices"},
    {"a", "mp_1", "mp_2", "mm_1", "mm_2"},    
    {"a", "mp_1", "mp_2", "m0_1", "m0_2", "cov_matrices"},
    {"a", "mp_1", "mp_2", "m0_1", "m0_2"},
]


def check_key_format_BCL(pars, require_m_star=True):
    """
    function to check the key format of BCL 1, 2, 3, 4
    """
    expected_keys = KEY_FORMAT_BCL if require_m_star else KEY_FORMAT_BCL_WITHOUT_M_STAR
    key = set(pars.keys())
    if key not in expected_keys:
        raise ValueError(f"Invalid parameter keys: expected one of {expected_keys}.")


def check_key_format_BCL_1(pars):
    check_key_format_BCL(pars, True)


def check_key_format_BCL_2(pars):
    check_key_format_BCL(pars, False)


def check_key_format_BCL_3(pars):
    check_key_format_BCL(pars, False)


def check_key_format_BCL_4(pars):
    check_key_format_BCL(pars, True)


### format the parameters
# pars from YAML -> standard pars




def format_mass_key(pars):
    """
    format mass keys: {m_1, m_2} -> {mp_1, mp_2, mm_1, mm_2}

    Return:
        pars: formatted parameters
    """
    if {"m_1", "m_2"}.issubset(pars.keys()):
        pars["mp_1"] = pars["mm_1"] = pars["m_1"]
        pars["mp_2"] = pars["mm_2"] = pars["m_2"]
        del pars["m_1"]
        del pars["m_2"]
    return pars


def add_t0_definition(pars):
    """
    add key for the definitions of t0

    Return:
        pars: parameters after adding the key "t0 def"
    """
    mass_cases = [{"mp_1", "mp_2", "mm_1", "mm_2"}, {"mp_1", "mp_2", "m0_1", "m0_2"}]
    if mass_cases[0].issubset(pars.keys()):
        pars["t0 def"] = 1
    elif mass_cases[1].issubset(pars.keys()):
        pars["t0 def"] = 2
    return pars


def format_parameter(pars):
    """
    format the parameters

    Return:
        pars: formatted parameters
    """
    pars = format_mass_key(pars)
    # after using this function, the keys could be
    # {mp_1, mp_2, mm_1, mm_2} (t0 def: 1)
    # {mp_1, mp_2, m0_1, m0_2} (t0 def: 2)
    pars = add_t0_definition(pars)
    return pars


def format_parameter_BCL(pars, bcl_type):
    """
    general function to format the parameters of BCL parameterization

    Args:
        pars: parameters to be formatted
        bcl_type: type of BCL parameterization, 1, 2, 3, 4
    """

    # check the key format
    check_functions = {
        1: check_key_format_BCL_1,
        2: check_key_format_BCL_2,
        3: check_key_format_BCL_3,
        4: check_key_format_BCL_4,
    }
    check_functions[bcl_type](pars)

    # format the parameters
    return format_parameter(pars)


def format_parameter_BCL_1(pars):
    return format_parameter_BCL(pars, 1)


def format_parameter_BCL_2(pars):
    return format_parameter_BCL(pars, 2)


def format_parameter_BCL_3(pars):
    return format_parameter_BCL(pars, 3)


def format_parameter_BCL_4(pars):
    return format_parameter_BCL(pars, 4)


### functions relevant for BCL paramerization
def get_tp(pars):
    """
    get the tp parameter
    """
    mp_1 = pars.get("mp_1") 

    mp_2 = pars.get("mp_2")

    return (mp_1 + mp_2) ** 2


def get_tm(pars):
    """
    get the tm parameter
    """
    mm_1 = pars.get("mm_1")
    mm_2 = pars.get("mm_2")
    return (mm_1 - mm_2) ** 2


def get_t0_1(pars):
    """
    get the t0 parameter by using definition 1
    """
    tp = get_tp(pars)
    tm = get_tm(pars)
    return tp - sqrt(tp * (tp - tm))



def get_t0_2(pars):
    """
    get the t0 parameter by using definition 2
    """
    m0_1 = pars.get("m0_1")
    m0_2 = pars.get("m0_2")
    return (m0_1 - m0_2) ** 2


### t0 parameter
def get_t0(pars):
    """
    get the t0 parameter with the help of 't0 def' parameter
    """
    if pars.get("t0 def") == 1:
        return get_t0_1(pars)
    elif pars.get("t0 def") == 2:
        return get_t0_2(pars)
    else:
        raise ValueError(f"Invalid t0 definition: {pars.get('t0 def')}")


def get_z(qsq, pars):
    """
    get the z parameter
    """
    tp = get_tp(pars)
    t0 = get_t0(pars)
    return (sqrt(1 - qsq / tp) - sqrt(1 - t0 / tp)) / (sqrt(1 - qsq / tp) + sqrt(1 - t0 / tp))


def get_z1(qsq, pars):
    """
    get the z in z expansions

    """
    m1 = pars.get("m_1")
    m2 = pars.get("m_2")
    t_plus = (m1 + m2) ** 2
    t0 = (m1 + m2) * (np.sqrt(m1) - np.sqrt(m2)) ** 2
    sqrt_tp_q = np.sqrt(t_plus - qsq)
    sqrt_tp_t0 = np.sqrt(t_plus - t0)
    z = (sqrt_tp_q - sqrt_tp_t0) / (sqrt_tp_q + sqrt_tp_t0)
    return z


def f_horgan_2015(qsq, pars):
    """Central-value fit used for the 2015 B -> V lattice form factors."""
    m_initial = pars.get("m_initial")
    m_final = pars.get("m_final")
    t0 = pars.get("t0")
    dm = pars.get("dm") / 1000.0
    a0, a1 = pars.get("a")

    t_plus = (m_initial + m_final) ** 2
    sqrt_tplus_qsq = np.sqrt(t_plus - qsq)
    sqrt_tplus_t0 = np.sqrt(t_plus - t0)
    z = (sqrt_tplus_qsq - sqrt_tplus_t0) / (sqrt_tplus_qsq + sqrt_tplus_t0)
    pole_mass = m_initial + dm
    return (a0 + a1 * z) / (1 - qsq / pole_mass**2)


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_1(qsq, pars):
    """
    function of the parameterization BCL 1
    """
    z = get_z(qsq, pars)  # not checked
    m_star = pars.get("m_star")
    a_list = pars.get("a")
    N = len(a_list)
    return sum(
        1 / (1 - qsq / m_star**2) * a * (z**n - (-1) ** (n - N) * (n / N) * z**N)
        for n, a in enumerate(a_list)
    )


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_2(qsq, pars):
    """
    function of the parameterization BCL 2
    """
    z = get_z(qsq, pars)  # not checked
    a_list = pars.get("a")
    N = len(a_list)
    return sum(a * (z**n - (-1) ** (n - N) * (n / N) * z**N) for n, a in enumerate(a_list))


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_3(qsq, pars):
    """
    function of the parameterization BCL 3
    """
    z = get_z(qsq, pars)  # not checked
    a_list = pars.get("a")
    return sum(a * z**n for n, a in enumerate(a_list))


# parameterization: BCL_4
# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_4(qsq, pars):
    """
    function of the parameterization BCL 4
    """
    z = get_z(qsq, pars)  # not checked
    m_star = pars.get("m_star")
    a_list = pars.get("a")
    return sum(1 / (1 - qsq / m_star**2) * a * z**n for n, a in enumerate(a_list))


def add_a0_last_from_ap(f_0, pars_0, f_p, pars_p):
    """
    add a0_N-1 from ap by using the relation f_p(0) = f_0(0) and return the new pars_0

    Args:
        f_0: function of the form factor f0, e.g., f_BCL_3
        pars_0: parameters of the form factor f0
        f_p: function of the form factor f+, e.g., f_BCL_1
        pars_p: parameters of the form factor f+

    Return:
        pars_0: parameters of the form factor f0 after adding a0_N-1
    """

    # get the a0_list of f0
    a0_list = pars_0.get("a")

    a0_list_auxiliary = [0] * (len(a0_list) + 1)
    a0_list_auxiliary[-1] = 1

    pars_0_auxiliary = deepcopy(pars_0)
    pars_0_auxiliary["a"] = a0_list_auxiliary

    last_coef_of_f_0 = f_0(0.0, pars_0_auxiliary)

    f_0_0 = f_0(0.0, pars_0)
    f_p_0 = f_p(0.0, pars_p)

    a0_last = (f_p_0 - f_0_0)/last_coef_of_f_0

    pars_0["a"].append(a0_last)

    return pars_0

# old function, not used
# When the keys satisfy the following conditions:
# 1. a0_last = 'by_ap'
# 2. f+.parameterization = 'BCL 1'
# 3. f0.parameterization = 'BCL 2' or 'BCL 3'
# the main program should call this function to update f0.a
'''
def add_a0_N_minus_1_from_ap(pars_p, pars_0):
    """
    add a0_N-1 from ap by using the relation f_p(0) = f_0(0)

    Args:
        pars_p: parameters of the form factor f+
        pars_0: parameters of the form factor f0
    """
    z0 = get_z(0.0, pars_0)
    N = len(pars_p.get("a"))  # N is the number of ap in the parameterization
    fp_0 = f_BCL_1(0.0, pars_p)  # f_p(0)
    a0_list = pars_0.get("a")  # a0_1, a0_2, ..., a0_N-2
    a0_N_minus_1 = (fp_0 - sum(a * z0**n for n, a in enumerate(a0_list[:-1]))) * z0 ** (1 - N)
    pars_0["a"].append(a0_N_minus_1)
    return pars_0
'''
    
def f_z_expansions_1(qsq, pars):
    z = get_z1(qsq, pars)
    z0 = get_z1(0, pars)
    f0 = pars.get("f(0)")
    c = pars.get("c")
    P = pars.get("P")
    term = (z - z0) * (1 + (z + z0)/2);
    f = (f0 + c * term) / (1 - P * qsq);

    
    return f


def f_z_expansions_2(qsq, pars):
    z = get_z1(qsq, pars)
    z0 = get_z1(0, pars)
    f0 = pars.get("f(0)")
    c = pars.get("c")
    Ms = pars.get("m_star")
    term = (z - z0) * (1 + (z + z0)/2);
    f = (f0 + c * term) / (1 -  qsq/Ms**2);

    return f


def f_z_expansions_3(qsq, pars):
    z = get_z1(qsq, pars)
    z0 = get_z1(0, pars)
    f0 = pars.get("f(0)")
    c = pars.get("c")
    term = (z - z0) * (1 + (z + z0)/2);
    f = f0 + c * term;

    return f

#求误差，先对函数求梯度
def df_da(qsq, pars, class_func):
    """计算形因子对参数的解析导数（返回梯度向量）"""
    if class_func == "Horgan 2015":
        m_initial = pars.get("m_initial")
        m_final = pars.get("m_final")
        t0 = pars.get("t0")
        dm = pars.get("dm") / 1000.0
        _, a1 = pars.get("a")
        t_plus = (m_initial + m_final) ** 2
        sqrt_tplus_qsq = np.sqrt(t_plus - qsq)
        sqrt_tplus_t0 = np.sqrt(t_plus - t0)
        z = (sqrt_tplus_qsq - sqrt_tplus_t0) / (sqrt_tplus_qsq + sqrt_tplus_t0)
        pole_mass = m_initial + dm
        pole_factor = 1 / (1 - qsq / pole_mass**2)
        return np.asarray([pole_factor, pole_factor * z], dtype=float)

    if class_func.startswith("z-expansions"):
        return df_dz_expansion(qsq, pars, class_func)

    z = get_z(qsq, pars) 
    m_star = pars.get("m_star")
    a_list = pars.get("a")
        # 处理复数情况
    if m_star != None:  # 考虑没有极点的公式
        pole_factor = 1 / (1 - qsq / m_star**2)
    else:
        pole_factor=1

    
    # 梯度向量：df/da0 = pole_factor * 1
    #           df/da1 = pole_factor * z
    #           df/da2 = pole_factor * z^2
    #           ...
    N = len(a_list)
    if class_func in ("BCL 1", "BCL 2"):
        grad = [pole_factor * (z**i - (-1) ** (i - N) * (i / N) * z**N) for i in range(len(a_list))]
    else:
        grad = [pole_factor * (z** i) for i in range(len(a_list))]
    return np.array(grad)


def _dz_expansion_value(qsq, pars, class_func):
    """Evaluate a z-expansion while keeping the parameter dictionary isolated."""
    functions = {
        "z-expansions 1": f_z_expansions_1,
        "z-expansions 2": f_z_expansions_2,
        "z-expansions 3": f_z_expansions_3,
    }
    try:
        return functions[class_func](qsq, pars)
    except KeyError as exc:
        raise ValueError(f"Invalid z-expansion parameterization: {class_func}") from exc


def df_dz_expansion(qsq, pars, class_func):
    """Return the gradient in the parameter order used by each z-expansion."""
    z = get_z1(qsq, pars)
    z0 = get_z1(0, pars)
    term = (z - z0) * (1 + (z + z0) / 2)
    dterm = 1 + z - z0
    f0 = pars.get("f(0)")
    c = pars.get("c")

    if class_func == "z-expansions 1":
        denominator = 1 - pars.get("P") * qsq
        gradient = [1 / denominator, term / denominator, (f0 + c * term) * qsq / denominator**2]
    elif class_func == "z-expansions 2":
        m_star = pars.get("m_star")
        denominator = 1 - qsq / m_star**2
        gradient = [1 / denominator, term / denominator, (f0 + c * term) * (-2 * qsq / m_star**3) / denominator**2]
    elif class_func == "z-expansions 3":
        gradient = [1.0, term]
    else:
        raise ValueError(f"Invalid z-expansion parameterization: {class_func}")
    return np.asarray(gradient, dtype=float)

# 改进的误差传播计算（解析导数）
def sigma_f_analytical(
    qsq,
    pars,
    cov_a,
    class_func,
    gradient_indices=None,
    gradient_local_indices=None,
):
    """
    解析计算形因子误差（基于解析导数）
    """
    q2_array = np.atleast_1d(qsq)
    errors = np.zeros_like(q2_array, dtype=float)

    for i, q2_val in enumerate(q2_array):
        grad = df_da(q2_val, pars, class_func)  # 梯度向量 [df/dp0, df/dp1, ...]
        if gradient_indices is not None:
            projected_grad = np.zeros(len(cov_a), dtype=float)
            local_indices = gradient_local_indices or range(len(gradient_indices))
            for local_index, global_index in zip(local_indices, gradient_indices):
                projected_grad[global_index] = grad[local_index]
            grad = projected_grad
        if len(grad) != len(cov_a):
            raise ValueError(
                f"Covariance matrix dimension ({len(cov_a)}) does not match "
                f"the {class_func} gradient dimension ({len(grad)})."
            )
        errors[i] = np.sqrt(np.dot(grad, np.dot(cov_a, grad)))
    
    return errors if len(q2_array) > 1 else errors[0]


def calculate_systematic_error_v2(O, O_HO, sigma_O, sigma_O_HO, *args, **kwargs):
        """
        支持传入函数表达式或具体数值
        如果是函数，会使用 *args 和 **kwargs 作为函数的参数进行求值
        """
        # 辅助函数：如果是可调用的函数，则求值；否则直接返回原值
        def evaluate(param):
            if callable(param):
                return param(*args, **kwargs)
            return param
        
        # 统一进行求值
        val_O = evaluate(O)
        val_O_HO = evaluate(O_HO)
        val_sigma_O = evaluate(sigma_O)
        val_sigma_O_HO = evaluate(sigma_O_HO)
        
        # 原有的计算逻辑
        diff = abs(val_O_HO - val_O)
        if val_sigma_O_HO >= val_sigma_O:
            second_term = np.sqrt(val_sigma_O_HO**2 - val_sigma_O**2)
        else:
            second_term = 0
            
        return np.maximum(diff, second_term)  

def calculate_total_error(sigma_O_stat, sigma_O_syst):
        """
        计算总误差 σ_O,tot
        
        参数:
        sigma_O_stat -- 统计误差
        sigma_O_syst -- 系统误差
        
        返回:
        总误差 σ_O,tot
        """
        return np.sqrt(sigma_O_stat**2 + sigma_O_syst**2)


