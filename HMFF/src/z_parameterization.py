from math import sqrt

# z parameterization
# see the equation in the note

### check format of the parameters

# key format of BCL
# m_star is optional
KEY_FORMAT_BCL = [
    {"a", "m_star", "m_1", "m_2"},
    {"a", "m_star", "mp_1", "mp_2", "mm_1", "mm_2"},
    {"a", "m_star", "mp_1", "mp_2", "m0_1", "m0_2"},
]

KEY_FORMAT_BCL_WITHOUT_M_STAR = [
    {"a", "m_1", "m_2"},
    {"a", "mp_1", "mp_2", "mm_1", "mm_2"},
    {"a", "mp_1", "mp_2", "m0_1", "m0_2"},
]


def check_key_format_BCL(pars, require_m_star=True):
    expected_keys = KEY_FORMAT_BCL if require_m_star else KEY_FORMAT_BCL_WITHOUT_M_STAR
    key = set(pars.keys())
    if key not in expected_keys:
        raise ValueError(f"Invalid parameter keys: expected one of {expected_keys}.")


# function to check the key format of BCL 1, 2, 3, 4
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


# format mass keys
# {m_1, m_2} -> {mp_1, mp_2, mm_1, mm_2}
def format_mass_key(pars):
    if {"m_1", "m_2"}.issubset(pars.keys()):
        pars["mp_1"] = pars["mm_1"] = pars["m_1"]
        pars["mp_2"] = pars["mm_2"] = pars["m_2"]
        del pars["m_1"]
        del pars["m_2"]
    return pars


# add key for the definitions of t0
def add_t0_definition(pars):
    mass_cases = [{"mp_1", "mp_2", "mm_1", "mm_2"}, {"mp_1", "mp_2", "m0_1", "m0_2"}]
    if mass_cases[0].issubset(pars.keys()):
        pars["t0 def"] = 1
    elif mass_cases[1].issubset(pars.keys()):
        pars["t0 def"] = 2
    return pars


# format the parameters
def format_parameter(pars):
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


# functions to format the parameters of BCL 1, 2, 3, 4
def format_parameter_BCL_1(pars):
    return format_parameter_BCL(pars, 1)


def format_parameter_BCL_2(pars):
    return format_parameter_BCL(pars, 2)


def format_parameter_BCL_3(pars):
    return format_parameter_BCL(pars, 3)


def format_parameter_BCL_4(pars):
    return format_parameter_BCL(pars, 4)


### functions relevant for BCL paramerization
### tp parameter
def get_tp(pars):
    mp_1 = pars.get("mp_1")
    mp_2 = pars.get("mp_2")
    return (mp_1 + mp_2) ** 2


### tm parameter
def get_tm(pars):
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


def get_z(q2, pars):
    """
    get the z parameter
    """
    tp = get_tp(pars)
    t0 = get_t0(pars)
    return (sqrt(1 - q2 / tp) - sqrt(1 - t0 / tp)) / (sqrt(1 - q2 / tp) + sqrt(1 - t0 / tp))


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_1(q2, pars):
    """
    function of the parameterization BCL 1
    """
    z = get_z(q2, pars)  # not checked
    m_star = pars.get("m_star")
    a_list = pars.get("a")
    N = len(a_list)
    return sum(
        1 / (1 - q2 / m_star**2) * a * (z**n - (-1) ** (n - N) * (n / N) * z**N)
        for n, a in enumerate(a_list)
    )


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_2(q2, pars):
    """
    function of the parameterization BCL 2
    """
    z = get_z(q2, pars)  # not checked
    a_list = pars.get("a")
    N = len(a_list)
    return sum(a * (z**n - (-1) ** (n - N) * (n / N) * z**N) for n, a in enumerate(a_list))


# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), a_0, a_1, a_2, ..., a_N-1
def f_BCL_3(q2, pars):
    """
    function of the parameterization BCL 3
    """
    z = get_z(q2, pars)  # not checked
    a_list = pars.get("a")
    return sum(a * z**n for n, a in enumerate(a_list))


# parameterization: BCL_4
# pars: mm1_, mm_2, mp_1, mp_2 (m_1, m_2), m_star, a_0, a_1, a_2, ..., a_N-1
def f_BCL_4(q2, pars):
    """
    function of the parameterization BCL 4
    """
    z = get_z(q2, pars)  # not checked
    m_star = pars.get("m_star")
    a_list = pars.get("a")
    return sum(1 / (1 - q2 / m_star**2) * a * z**n for n, a in enumerate(a_list))


### function to get a0_N-1 from ap
# This function is used to get a0_N-1 from ap by using the relation f_p(0) = f_0(0)
# depending on both pars_p and pars_0
# When the keys satisfy the following conditions:
# 1. a0_last = 'by_ap'
# 2. f+.parameterization = 'BCL 1'
# 3. f0.parameterization = 'BCL 2' or 'BCL 3'
# the main program should call this function to update f0.a
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


def f_z_expansions_1(q2, pars):
    raise NotImplementedError


def f_z_expansions_2(q2, pars):
    raise NotImplementedError


def f_z_expansions_3(q2, pars):
    raise NotImplementedError
