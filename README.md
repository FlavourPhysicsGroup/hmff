# HMFF — Hadronic Matrix Form Factors

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)

HMFF is a Python library that collects and provides parameterized results of hadronic transition form factors from the literature. All form factors are given through various parameterization forms with parameter values taken from published references — the final form factor values are functions of the squared momentum transfer $q^2$ only. This project is distributed as a library for particle physics researchers to call directly.

[中文 README](README_CN.md)

## Architecture

The project uses a three-layer design:

| Layer | Class/Module | Description |
|-------|-------------|-------------|
| **Top** | `FormFactor` | Represents a physical process (e.g. $B \to K$), containing all literature implementations for that process |
| **Middle** | `Impl` | Represents the parameterized data from a single reference, containing all form factors from that paper |
| **Bottom** | Parameterization functions | Concrete mathematical parameterization forms (e.g. BCL 1, one pole, etc.), taking $q^2$ as input and returning form factor values |

For example, the $B \to K$ process corresponds to a `FormFactor` object that contains two literature implementations (`Impl`): LCSR-pole 2004 and LQCD-FLAG-2024. Each `Impl` in turn contains specific form factors such as $f_+$, $f_0$, $f_T$, each using a different parameterization function.

## Included Processes and References

### Pseudoscalar → Pseudoscalar (P → P)

| Process | Implementations |
|---------|----------------|
| $B \to \pi$ | LCSR-pole 2004, LQCD-FLAG-2024, LQCD-z 2015 |
| $B \to K$ | LCSR-pole 2004, LQCD-FLAG-2024 |
| $B \to \eta$ | LCSR-pole 2004 |
| $B_s \to K$ | LQCD-z 2015, LQCD-FLAG-2024 |
| $B \to D$ | LQCD-FLAG-2024 |
| $D \to \pi$ | LQCD-z 2017 |
| $D \to K$ | LQCD-z 2017 |

### Pseudoscalar → Vector (P → V)

| Process | Implementations |
|---------|----------------|
| $B \to \rho$ | LCSR-pole, LQCD-2008 |
| $B \to K^*$ | LCSR-pole, LQCD-2015 |
| $B \to \omega$ | LCSR-pole |
| $B_s \to K^*$ | LCSR-pole, LQCD-2015 |
| $B_s \to \phi$ | LCSR-pole, LQCD-2015 |

### Baryon → Baryon (B → B)

| Process | Implementations |
|---------|----------------|
| $\Lambda_b \to \Lambda$ | LQCD-2016-nominal, LQCD-2016-HO |
| $\Lambda_b \to \Lambda(1520)$ | LQCD-2021-nominal, LQCD-2021-HO |
| $\Xi_c \to \Xi$ | (TBD) |

## Supported Parameterization Forms

| Name | Formula | Description |
|------|---------|-------------|
| one pole | $f = a / (1 - q^2/m^2)$ | Single-pole parameterization |
| double pole 1 | $f = a_1/(1 - q^2/m_1^2) + a_2/(1 - q^2/m_2^2)$ | Double-pole (independent pole masses) |
| double pole 2 | $f = a_1/(1 - q^2/m^2) + a_2/(1 - q^2/m^2)^2$ | Double-pole (shared pole mass) |
| BCL 1 | Bourrely-Caprini-Lellouch (with pole factor and constraint) | Most common z-expansion |
| BCL 2 | BCL (with constraint, no pole factor) | |
| BCL 3 | BCL (pure z-expansion, no pole factor, no constraint) | |
| BCL 4 | BCL (with pole factor, no constraint) | |
| z-expansions 1/2/3 | Other z-expansion forms | Not yet implemented |

## Quick Start

### Install from PyPI (not yet published)

```bash
pip install hmff
```

or with uv:

```bash
uv pip install hmff
```

### Install from source

```bash
git clone https://github.com/FlaourPhysicsGroup/hmff.git
uv add /path/to/form-factor
```

### Usage Example

```python
import hmff

# Get all available processes
formfactors = hmff.formfactors
print(formfactors.keys())
# dict_keys(['B->rho', 'B->K*', ..., 'B->pi', 'B->K', ..., 'D->pi', 'D->K'])

# Get the $B \to K$ process
ff_bk = formfactors['B->K']

# See which references are included for this process
print(ff_bk.impl_names)  # ['LCSR-pole 2004', 'LQCD-FLAG-2024']

# Get a specific literature implementation
impl = ff_bk.get_impl('LQCD-FLAG-2024')
print(impl.ref)           # arXiv:2411.04268
print(impl.form_factor_names)  # ['f+', 'f0', 'fT']

# Compute the form factor value at $q^2 = 10\,\mathrm{GeV}^2$
func_fplus = impl.form_factor_function("f+")
print(func_fplus(qsq=10))  # 1.68

# Get all form factor values at a given $q^2$ simultaneously
print(impl.get_central_values(qsq=10))  # {f+: ..., f0: ..., fT: ...}
```

### Error Estimation

For references that provide covariance matrices (e.g. LQCD-FLAG-2024), statistical errors can be computed:

```python
sigma_func = impl.get_sigma_f_stat("f+")
print(sigma_func(qsq=10))  # statistical error
```

## Project Structure

```
src/hmff/
├── __init__.py          # Entry point: initializes the formfactors dict
├── classes.py           # FormFactor and Impl class definitions
├── data_io.py           # LazyFormFactorLoader for lazy-loading YAML data
├── z_parameterization.py  # BCL and z-expansion parameterization functions
├── pole_dominance.py    # Pole-dominance parameterization functions
└── data/
    ├── P_P.yaml         # Pseudoscalar → pseudoscalar process data
    ├── P_V.yaml         # Pseudoscalar → vector process data
    └── B_B.yaml         # Baryon → baryon process data
```

## Data Format

All form factor data is stored in YAML files with the following format:

```yaml
B->K:
  LQCD-FLAG-2024:
    ref: arXiv:2411.04268
    method: LQCD
    form factors:
      f+:
        parameterization: BCL 2
        parameter: {a: [0.0, 0.1, ...], mp_1: 5.28, mp_2: 0.494, m_star: 5.37,
                    cov_matrices: [[...], [...]]}
      f0:
        parameterization: BCL 3
        parameter: {a: [0.0, 0.1, ...], mp_1: 5.28, mp_2: 0.494}
```

Mass parameters in `parameter` can use either `m` or `m_sq` (the program converts automatically). Covariance matrices are optional.

## Development

This project uses uv for dependency management:

```bash
# Install dev dependencies
uv sync --group dev

# Run tests
uv run pytest tests/
```

## License

This project is licensed under GPLv3. See [LICENSE](LICENSE) for details.
