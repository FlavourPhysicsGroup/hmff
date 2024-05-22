"""FLAG_Review_2021"""
import math
import yaml
import codecs
from pathlib import Path
from .classes import Impl
from .initialization import formfactors

# 定义初始值
m1 = {'B': 5.27966, 'Bs': 5.36692}
m2 = {'pi': 0.134977, 'K': 0.495644, 'D': 1.86966}
mBstar = 5.3252
mBstar_0p = 5.63

# 从文件中加载参数
with codecs.open(Path(__file__).parent / 'data/FLAG_Review_2021.yaml', 'r',
                 encoding='utf-8') as file:
    ff_pars = yaml.load(file, yaml.SafeLoader)


def z(q2, IS, FS):
    # ref: eq.524
    tp = (m1.get(IS) + m2.get(FS))**2
    t0 = (m1.get(IS) + m2.get(FS)) * (math.sqrt(m1.get(IS)) - math.sqrt(m2.get(FS)))**2
    return (math.sqrt(tp - q2) - math.sqrt(tp - t0)) / (math.sqrt(tp - q2) + math.sqrt(tp - t0))


def z1(qs, IS, FS):
    tp = (m1.get(IS) + m2.get(FS))**2
    tm = (m1.get(IS) - m2.get(FS))**2
    t0 = tp - math.sqrt(tp * (tp - tm))
    return (math.sqrt(tp - qs) - math.sqrt(tp - t0)) / (math.sqrt(tp - qs) + math.sqrt(tp - t0))


def fpBCL(IS, FS, q2, pars):
    # ref: eq.533
    ap = pars
    result = 0
    for n in range(0, 3):
        term = (z(q2, IS, FS)**n - (-1)**(n - 3) * n / 3 * z(q2, IS, FS)**3) * ap[n]
        result += term
    return 1 / (1 - q2 / mBstar**2) * result


def f0BCL(IS, FS, q2, pars):
    # ref: eq.534
    a0 = pars
    result = 0
    for n in range(0, 3):
        term = a0[n] * z(q2, IS, FS)**n
        result += term
    return result


def fpBCL4(IS, FS, qs, pars):
    # ref: eq.533
    ap = pars
    result = 0
    for n in range(0, 4):  # 根据N修改
        term = (z1(qs, IS, FS)**n - (-1)**(n - 4) * n / 4 * z1(qs, IS, FS)**4) * ap[n]
        result += term
    return 1 / (1 - qs / mBstar**2) * result


def f0BCL4(IS, FS, qs, pars):
    # ref: eq.534
    a0 = pars
    result = 0
    for n in range(0, 4):
        term = a0[n] * z1(qs, IS, FS)**n
        result += term
    return result


def ff(process, q2):
    parts = process.split('->')
    IS = parts[0]
    FS = parts[1]
    if 'B->pi' in process:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['ap']),
            'f0': f0BCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['a0']),
            'fT': fpBCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['aT']),
        }
        return _ff
    elif 'Bs->K' in process:
        _ff = {
            'f+': fpBCL4(IS, FS, q2, pars=ff_pars[process + ' form factor']['ap']),
            'f0': f0BCL4(IS, FS, q2, pars=ff_pars[process + ' form factor']['a0']),
        }
        return _ff
    elif 'B->K' in process:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['ap']),
            'f0': f0BCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['a0']),
            'fT': fpBCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['aT']),
        }
    elif 'B->D' in process:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['ap']),
            'f0': f0BCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['a0']),
        }
    else:
        return {}


# 对4种过程，分别创建 Impl 对象，并分别记录在对应过程的 FormFactor 对象内。
for process in ['B->pi', 'B->K']:
    impl = Impl('z-param by FLAG Review 2021',
                ff_obj=formfactors[process],
                ff_names=['f+', 'f0', 'fT'],
                param_form='z-param',
                methods='LQCD',
                ref='FLAG Review 2021')
    impl.set_description = (f"用{impl.param_form}参数化和{impl.methods}方法，"
                            f"实现了{impl.ff_names}，参考了{impl.ref}")
    impl.set_func(lambda qsq: ff(process, qsq))
    formfactors[process].add_impl(impl)

for process in ['B->D', 'Bs->K']:
    impl = Impl('z-param by FLAG Review 2021',
                ff_obj=formfactors[process],
                ff_names=['f+', 'f0'],
                param_form='z-param',
                methods='LQCD',
                ref='FLAG Review 2021')
    impl.set_description = (f"用{impl.param_form}参数化和{impl.methods}方法，"
                            f"实现了{impl.ff_names}，参考了{impl.ref}")
    impl.set_func(lambda qsq: ff(process, qsq))
    formfactors[process].add_impl(impl)
