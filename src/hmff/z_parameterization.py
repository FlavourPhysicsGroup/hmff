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


def format_parameter_BCL_5(pars):
    """check the key format of the BCL 5 parameterization (LCSR-style):
    f(q^2) = (a0 + a1 z) / (1 - q^2/m_pole^2), with z using
    t0 = (m_initial - m_final)^2 = q^2_max (arXiv:2412.06515 LCSR
    Lambda_b -> Lambda(1520), Eq. (30)).
    """
    expected_keys = {"a0", "a1", "m_pole", "m_1", "m_2", "m_initial", "m_final"}
    if set(pars.keys()) != expected_keys:
        raise ValueError(
            f"Invalid parameter keys: expected {expected_keys}, got {set(pars.keys())}."
        )
    return pars


def f_BCL_5(qsq, pars):
    """BCL 5 (LCSR-style pole + z-series):
    f(q^2) = (a0 + a1 * z(q^2)) / (1 - q^2/m_pole^2)
    where z is evaluated with get_z using t0 definition 2,
    i.e. t0 = (m_initial - m_final)^2 = q^2_max (so z(q^2_max) = 0).
    """
    a0 = pars.get("a0")
    a1 = pars.get("a1")
    m_pole = pars.get("m_pole")
    # build a BCL-format parameter dict for get_z (t_+ from m_1/m_2, t0 def 2)
    z_pars = {
        "mp_1": pars.get("m_1"),
        "mp_2": pars.get("m_2"),
        "m0_1": pars.get("m_initial"),
        "m0_2": pars.get("m_final"),
        "t0 def": 2,
    }
    z = get_z(qsq, z_pars)
    return (a0 + a1 * z) / (1 - qsq / m_pole**2)


# ---------------------------------------------------------------------------
# BCL 5 (LCSR-style) — a0 endpoint relations (arXiv:2412.06515)
# ---------------------------------------------------------------------------
# For Lambda_b -> Lambda(1520) some form factors do not have an independent a0;
# it is fixed by the endpoint relations at q^2 = 0 or q^2 = q^2_max:
#   a0_fVt    = a0_fV0   + z(0) (a1_fV0   - a1_fVt)
#   a0_gAt    = a0_gA0   + z(0) (a1_gA0   - a1_gAt)
#   a0_gAperp = a0_gA0
#   a0_fTperp = a0_gTperp + z(0) (a1_gT0 - a1_fTperp)
#   a0_gT0    = a0_gTperp
# Here z(q^2_max) = 0 because t0 = q^2_max.  The order of the independent
# parameters in the published covariance matrix is stored in the YAML
# (covariance_matrix.order) rather than in code.

BCL5_A0_ENDPOINT_FFS = ("fVt", "gAt", "gAperp", "fTperp", "gT0")


def _z_bcl5(qsq, pars):
    """z with t0 = (m_initial - m_final)^2 (t0 definition 2), as used by f_BCL_5."""
    z_pars = {
        "mp_1": pars.get("m_1"),
        "mp_2": pars.get("m_2"),
        "m0_1": pars.get("m_initial"),
        "m0_2": pars.get("m_final"),
        "t0 def": 2,
    }
    return get_z(qsq, z_pars)


def bcl5_a0_endpoint_sources(ff_name, pars):
    """
    Return the sources of a0 for form factors whose a0 is determined by the
    endpoint relations of arXiv:2412.06515 (see comments above).
    Returns a list of (ff_name, param, coefficient), or None if the form
    factor has its own a0.
    """
    if ff_name not in BCL5_A0_ENDPOINT_FFS:
        return None
    z0 = _z_bcl5(0.0, pars)
    relations = {
        "fVt": [("fV0", "a0", 1.0), ("fV0", "a1", z0), ("fVt", "a1", -z0)],
        "gAt": [("gA0", "a0", 1.0), ("gA0", "a1", z0), ("gAt", "a1", -z0)],
        "gAperp": [("gA0", "a0", 1.0)],
        "fTperp": [("gTperp", "a0", 1.0), ("gT0", "a1", z0), ("fTperp", "a1", -z0)],
        "gT0": [("gTperp", "a0", 1.0)],
    }
    return relations.get(ff_name)


def bcl5_inject_masses(ff_data, config):
    """Inject m_initial/m_final from the impl-level config if missing."""
    if ff_data.get("m_initial") is None:
        ff_data["m_initial"] = config.get("m_initial")
    if ff_data.get("m_final") is None:
        ff_data["m_final"] = config.get("m_final")
    return ff_data


def bcl5_compute_a0(ff_name, ff_data, config):
    """Compute a0 from the endpoint relations if it is not independent."""
    sources = bcl5_a0_endpoint_sources(ff_name, ff_data)
    if sources is None:
        return ff_data  # the form factor has its own a0
    a0 = 0.0
    for src_ff, param, coef in sources:
        src_pars = deepcopy(config["form factors"][src_ff]["parameter"])
        a0 += coef * src_pars[param]
    ff_data["a0"] = a0
    return ff_data


def bcl5_prepare(ff_name, ff_data, config):
    """Inject masses and compute a0 via the endpoint relations (if needed)."""
    bcl5_inject_masses(ff_data, config)
    return bcl5_compute_a0(ff_name, ff_data, config)


def bcl5_linear_maps(ff_name, ff_data, index):
    """
    Return the linear maps of (a0, a1) onto the *global* covariance parameters.
    `index` maps (ff_name, param) -> global index (from covariance_matrix.order).
    Returns two lists of (global_index, coefficient).
    """
    z0 = _z_bcl5(0.0, ff_data)
    sources = bcl5_a0_endpoint_sources(ff_name, ff_data)
    if sources is None:
        a0_linear = [(index[(ff_name, "a0")], 1.0)]
    else:
        a0_linear = [
            (index[(src_ff, param)], coef) for src_ff, param, coef in sources
        ]
    a1_linear = [(index[(ff_name, "a1")], 1.0)]
    return a0_linear, a1_linear


def df_da_bcl5(qsq, pars):
    """
    Analytic gradient of a BCL 5 form factor w.r.t. the *global* covariance
    parameters (via the linear maps in pars['_a0_linear']/_a1_linear').
    """
    m_pole = pars.get("m_pole")
    z = _z_bcl5(qsq, pars)
    pole = 1.0 / (1.0 - qsq / m_pole**2)
    df_da0 = pole
    df_da1 = pole * z

    a0_linear = pars.get("_a0_linear", [])
    a1_linear = pars.get("_a1_linear", [])
    n = pars.get(
        "_bcl5_cov_dim",
        1 + max([idx for idx, _ in a0_linear + a1_linear], default=-1),
    )
    grad = np.zeros(n, dtype=float)
    for idx, coef in a0_linear:
        grad[idx] += df_da0 * coef
    for idx, coef in a1_linear:
        grad[idx] += df_da1 * coef
    return grad


# ---------------------------------------------------------------------------
# BCL 4 endpoint relations (e.g. Xi_c -> Xi, arXiv:2504.07302)
# ---------------------------------------------------------------------------
# The BCL-4 z-expansion f(q^2) = 1/(1 - q^2/m_pole^2) * (a0 + a1 z + a2 z^2 + a3 z^3)
# is sometimes used with helicity endpoint constraints that fix some of the
# coefficients. In the YAML a form factor declares which coefficient is
# dependent via the "endpoint" key, e.g.
#     f0:    endpoint: {a2: f+}     # a2 from f_0(0) = f_+(0)
#     g0:    endpoint: {a2: g+}     # a2 from g_0(0) = g_+(0)
#     gperp: endpoint: {a0: g+}     # a0 shared with g+
# The dependent coefficients are omitted from the "a" list in the YAML
# (f0/g0: [a0, a1, a3]; gperp: [a1, a2, a3]) and injected by bcl4_endpoint_prepare.
# For Xi_c -> Xi (arXiv:2504.07302) the z variable uses
#     t0 = q^2_max = (m_Xi_c - m_Xi)^2   (t0 definition 2),
#     t_+^{f+,fperp,f0} = (m_D + m_K)^2,  t_+^{g+,gperp,g0} = (m_D* + m_K)^2.


def _z_xic_xi(qsq, pars):
    """z with t_+ = (mp_1 + mp_2)^2 and t0 = (m0_1 - m0_2)^2 (t0 definition 2)."""
    z_pars = {
        "mp_1": pars.get("mp_1"),
        "mp_2": pars.get("mp_2"),
        "m0_1": pars.get("m0_1"),
        "m0_2": pars.get("m0_2"),
        "t0 def": 2,
    }
    return get_z(qsq, z_pars)


def bcl4_endpoint_prepare(ff_name, ff_data, endpoint_cfg, config):
    """
    Inject the endpoint-relation coefficients for a BCL-4 form factor.
    `endpoint_cfg` is the YAML "endpoint" dict, e.g. {"a2": "f+"} or {"a0": "g+"}.
    - {"a2": src}: compute a2 from f_ff(0) = f_src(0);
    - {"a0": src}: share a0 with the source form factor.
    """
    a = list(ff_data.get("a", []))
    if "a2" in endpoint_cfg:
        src_name = endpoint_cfg["a2"]
        src_a = list(config["form factors"][src_name]["parameter"]["a"])
        z0 = _z_xic_xi(0.0, ff_data)
        # f_src(0) = sum_n a_n z0^n  (the pole factor is 1 at q^2 = 0)
        f_src0 = sum(coef * z0 ** n for n, coef in enumerate(src_a))
        a0, a1 = a[0], a[1]
        a3 = a[2] if len(a) >= 3 else 0.0
        # f_ff(0) = a0 + a1 z0 + a2 z0^2 + a3 z0^3 = f_src(0)  =>  a2:
        a2 = (f_src0 - a0 - a1 * z0 - a3 * z0 ** 3) / z0 ** 2
        ff_data["a"] = [a0, a1, a2, a3]
    elif "a0" in endpoint_cfg:
        src_name = endpoint_cfg["a0"]
        src_a0 = config["form factors"][src_name]["parameter"]["a"][0]
        ff_data["a"] = [src_a0] + a
    return ff_data


def bcl4_endpoint_linear_maps(ff_name, ff_data, endpoint_cfg, index):
    """
    Return the linear maps of a0..a3 onto the *global* covariance parameters.
    `index` maps (ff_name, param) -> global index (from covariance_matrix.order).
    Returns a list of 4 lists of (global_index, coefficient).
    `endpoint_cfg` may be None/empty for independent BCL-4 coefficients.
    """
    endpoint_cfg = endpoint_cfg or {}
    z0 = _z_xic_xi(0.0, ff_data)
    z02 = z0 ** 2
    i = index

    if "a2" in endpoint_cfg:
        src = endpoint_cfg["a2"]
        # a2 = (f_src(0) - a0 - a1 z0 - a3 z0^3)/z0^2,  f_src(0)=sum_n src_a_n z0^n
        a2_map = [
            (i[(src, "a0")], 1.0 / z02),
            (i[(src, "a1")], 1.0 / z0),
            (i[(src, "a2")], 1.0),
            (i[(src, "a3")], z0),
            (i[(ff_name, "a0")], -1.0 / z02),
            (i[(ff_name, "a1")], -1.0 / z0),
            (i[(ff_name, "a3")], -z0),
        ]
        return [
            [(i[(ff_name, "a0")], 1.0)],
            [(i[(ff_name, "a1")], 1.0)],
            a2_map,
            [(i[(ff_name, "a3")], 1.0)],
        ]

    if "a0" in endpoint_cfg:
        src = endpoint_cfg["a0"]
        # a0 is shared with the source form factor
        return [
            [(i[(src, "a0")], 1.0)],
            [(i[(ff_name, "a1")], 1.0)],
            [(i[(ff_name, "a2")], 1.0)],
            [(i[(ff_name, "a3")], 1.0)],
        ]

    # independent BCL-4 coefficients
    return [
        [(i[(ff_name, "a0")], 1.0)],
        [(i[(ff_name, "a1")], 1.0)],
        [(i[(ff_name, "a2")], 1.0)],
        [(i[(ff_name, "a3")], 1.0)],
    ]


def df_da_bcl4_xicxi(qsq, pars):
    """
    Analytic gradient of a Xi_c -> Xi BCL-4 form factor w.r.t. the *global*
    covariance parameters (via the linear maps in pars['_xicxi_a_linear']).
    """
    m_star = pars.get("m_star")
    z = _z_xic_xi(qsq, pars)
    pole = 1.0 / (1.0 - qsq / m_star ** 2)

    a_linear = pars.get("_xicxi_a_linear", [])
    all_coefs = [item for sublist in a_linear for item in sublist]
    n = pars.get(
        "_xicxi_cov_dim",
        1 + max([idx for idx, _ in all_coefs], default=-1),
    )
    grad = np.zeros(n, dtype=float)
    for n_a, coefs in enumerate(a_linear):
        df_da_n = pole * z ** n_a
        for idx, coef in coefs:
            grad[idx] += df_da_n * coef
    return grad


#求误差，先对函数求梯度
def df_da(qsq, pars, class_func):
    """计算形因子对参数的解析导数（返回梯度向量）"""
    if class_func == "pole w expansion":
        from .pole_w_expansion import df_da as df_da_pole_w
        return df_da_pole_w(qsq, pars)
    if class_func == "BCL 5":
        # a0 may be fixed by the endpoint relations -> gradient via linear maps
        return df_da_bcl5(qsq, pars)
    if class_func == "BCL 4" and pars.get("_xicxi_a_linear") is not None:
        # a2 (f0/g0) and a0 (gperp) may be fixed by the endpoint relations
        return df_da_bcl4_xicxi(qsq, pars)
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


