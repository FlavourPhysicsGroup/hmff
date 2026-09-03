"""
Pole + (w-1) expansion parameterization for heavy-baryon -> excited-baryon
transitions (a generic parameterization *type*, e.g. Lambda_b -> Lambda(1520),
Lambda_c -> Lambda(1520), Lambda_b -> Lambda_c*(2595,2625), ...),
following arXiv:2107.13140 (Meinel & Rendon).

The form factors are parametrized as
    f(q^2) = 1/(1 - q^2/m_pole^2) * sum_n a_n (w-1)^n ,
with
    w = (m_initial^2 + m_final^2 - q^2) / (2 m_initial m_final) ,
so that w = 1 (i.e. w - 1 = 0) corresponds to q^2 = q^2_max =
(m_initial - m_final)^2.

For a J^P = 1/2^+ -> 3/2^- final state, some form factors do not have an
independent a0; their a0 is fixed by the endpoint relations at q^2_max
(arXiv:2107.13140, Eqs. (24)-(30)).  These relations are process-independent
(given only the initial/final masses).  The *order* of the independent
parameters in the published covariance matrix is process-specific and is
therefore stored in the YAML (covariance_matrix.order) rather than in code.
"""

from copy import deepcopy

import numpy as np

# ---------------------------------------------------------------------------
# value & format functions
# ---------------------------------------------------------------------------

def get_w(qsq, pars):
    """return the recoil variable w for the given q^2"""
    m_initial = pars.get("m_initial")
    m_final = pars.get("m_final")
    return (m_initial**2 + m_final**2 - qsq) / (2 * m_initial * m_final)


def format_parameters_pole_w_expansion(pars):
    """check the key format of the pole + (w-1) expansion parameterization"""
    expected_keys = {"a0", "a1", "m_pole", "m_initial", "m_final"}
    if set(pars.keys()) != expected_keys:
        raise ValueError(
            f"Invalid parameter keys: expected {expected_keys}, got {set(pars.keys())}."
        )
    return pars


def f_pole_w_expansion(qsq, pars):
    """pole + (w-1) expansion:
    f(q^2) = 1/(1 - q^2/m_pole^2) * (a0 + a1*(w-1))
    """
    a0 = pars.get("a0")
    a1 = pars.get("a1")
    m_pole = pars.get("m_pole")
    w = get_w(qsq, pars)
    pole = 1.0 / (1.0 - qsq / m_pole**2)
    return pole * (a0 + a1 * (w - 1))


# ---------------------------------------------------------------------------
# endpoint relations (a0 elimination) for a 1/2^+ -> 3/2^- final state
# ---------------------------------------------------------------------------

def a0_endpoint_sources(ff_name, m_initial, m_final):
    """
    Return the sources of a0 for form factors whose a0 is *not* an independent
    parameter, i.e. it is determined by the endpoint relations at q^2_max of
    arXiv:2107.13140, Eqs. (24)-(30):
        a0_f+   = 2(m_i-m_f)/(m_i+m_f) * a0_fpp
        a0_fp   = - a0_fpp
        a0_g0   = 0
        a0_g+   = a0_gp - a0_gpp
        a0_h+   = 2(m_i+m_f)/(m_i-m_f) * a0_hpp
        a0_hp   = - a0_hpp
        a0_ht+  = a0_htp - a0_htpp
    Returns a list of (ff_name, param, coefficient), or None if the form
    factor has its own a0.
    """
    r_f = 2.0 * (m_initial - m_final) / (m_initial + m_final)
    r_h = 2.0 * (m_initial + m_final) / (m_initial - m_final)
    relations = {
        "f+": [("fpp", "a0", r_f)],
        "fp": [("fpp", "a0", -1.0)],
        "g0": [],
        "g+": [("gp", "a0", 1.0), ("gpp", "a0", -1.0)],
        "h+": [("hpp", "a0", r_h)],
        "hp": [("hpp", "a0", -1.0)],
        "ht+": [("htp", "a0", 1.0), ("htpp", "a0", -1.0)],
    }
    return relations.get(ff_name)  # None if the form factor has its own a0


# ---------------------------------------------------------------------------
# helpers operating on a form-factor parameter dict and the impl config (YAML)
# ---------------------------------------------------------------------------

def inject_masses(ff_data, config):
    """
    Inject the initial/final baryon masses into ff_data.
    Prefer the form factor's own m_initial/m_final (already in the YAML
    parameters); fall back to the impl-level config if missing.
    """
    if ff_data.get("m_initial") is None:
        ff_data["m_initial"] = config.get("m_initial")
    if ff_data.get("m_final") is None:
        ff_data["m_final"] = config.get("m_final")
    return ff_data


def compute_a0(ff_name, ff_data, config):
    """
    If the form factor's a0 is not an independent parameter (determined by the
    endpoint relations), compute it from the other form factors' a0 according
    to arXiv:2107.13140 Eqs. (24)-(30) and add it to ff_data.
    """
    sources = a0_endpoint_sources(
        ff_name, ff_data.get("m_initial"), ff_data.get("m_final")
    )
    if sources is None:
        return ff_data  # the form factor has its own a0
    a0 = 0.0
    for src_ff, _param, coef in sources:
        src_pars = deepcopy(config["form factors"][src_ff]["parameter"])
        a0 += coef * src_pars["a0"]
    ff_data["a0"] = a0
    return ff_data


def prepare(ff_name, ff_data, config):
    """inject masses and compute a0 via the endpoint relations (if needed)."""
    inject_masses(ff_data, config)
    return compute_a0(ff_name, ff_data, config)


def linear_maps(ff_name, ff_data, index):
    """
    Return the linear maps of (a0, a1) onto the *global* covariance
    parameters.  `index` maps (ff_name, param) -> global index (built from the
    covariance_matrix.order stored in the YAML).
    Returns two lists of (global_index, coefficient).
    """
    sources = a0_endpoint_sources(
        ff_name, ff_data.get("m_initial"), ff_data.get("m_final")
    )
    if sources is None:
        a0_linear = [(index[(ff_name, "a0")], 1.0)]
    else:
        a0_linear = [
            (index[(src_ff, param)], coef) for src_ff, param, coef in sources
        ]
    a1_linear = [(index[(ff_name, "a1")], 1.0)]
    return a0_linear, a1_linear


def df_da(qsq, pars):
    """
    Analytic gradient of a "pole w expansion" form factor w.r.t. the *global*
    covariance parameters.

    For form factors whose a0 is determined by the endpoint relations, the
    gradient is built via the linear maps stored in pars under '_a0_linear'
    and '_a1_linear' (each a list of (global_index, coefficient)).
    """
    m_pole = pars.get("m_pole")
    m_initial = pars.get("m_initial")
    m_final = pars.get("m_final")
    w = (m_initial**2 + m_final**2 - qsq) / (2 * m_initial * m_final)
    pole = 1.0 / (1.0 - qsq / m_pole**2)
    df_da0 = pole
    df_da1 = pole * (w - 1)

    a0_linear = pars.get("_a0_linear", [])
    a1_linear = pars.get("_a1_linear", [])
    n = pars.get(
        "_pole_w_cov_dim",
        1 + max([idx for idx, _ in a0_linear + a1_linear], default=-1),
    )
    grad = np.zeros(n, dtype=float)
    for idx, coef in a0_linear:
        grad[idx] += df_da0 * coef
    for idx, coef in a1_linear:
        grad[idx] += df_da1 * coef
    return grad
