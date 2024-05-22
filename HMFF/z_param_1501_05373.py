"""参考1501.05373 [hep-lat]"""
import math
import yaml
import codecs
from pathlib import Path
from .classes import Impl
from .initialization import formfactors

# 定义初始值
m1 = {'B': 5.27966, 'Bs': 5.36692}
m2 = {'pi': 0.134977, 'K': 0.495644}
mBstar = 5.3252
mBstar_0p = 5.63

# 从文件中加载参数
with codecs.open(Path(__file__).parent / 'data/Flynn_Izubuchi.yaml', 'r', encoding='utf-8') as file:
    ff_pars = yaml.load(file, yaml.SafeLoader)


def z(q2, IS, FS):
    # ref: eq.39
    tp = (m1.get(IS) + m2.get(FS))**2
    t0 = (m1.get(IS) + m2.get(FS)) * (math.sqrt(m1.get(IS)) - math.sqrt(m2.get(FS)))**2
    return (math.sqrt(tp - q2) - math.sqrt(tp - t0)) / (math.sqrt(tp - q2) + math.sqrt(tp - t0))


def fpBCL(IS, FS, q2, pars):
    # ref: eq.44
    ap = pars
    result = 0
    for n in range(0, 3):
        term = (z(q2, IS, FS)**n - (-1)**(n - 3) * n / 3 * z(q2, IS, FS)**3) * ap[n]
        result += term
    return 1 / (1 - q2 / mBstar**2) * result


def f0BCL(IS, FS, q2, pars):
    # ref: eq.45
    a0 = pars
    result = 0
    for n in range(0, 3):
        term = a0[n] * z(q2, IS, FS)**n
        result += term
    return result


def f0BCL1(IS, FS, q2, pars):
    # ref: eq.46
    a0 = pars
    result = 0
    for n in range(0, 3):
        term = a0[n] * z(q2, IS, FS)**n
        result += term
    return 1 / (1 - q2 / mBstar_0p**2) * result


def ff(process, q2):
    parts = process.split('->')
    IS = parts[0]
    FS = parts[1]
    if 'B->pi' in process:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['ap']),
            'f0': f0BCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['a0']),
        }
        return _ff
    elif 'Bs->K' in process:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[process + ' form factor']['ap']),
            'f0': f0BCL1(IS, FS, q2, pars=ff_pars[process + ' form factor']['a0']),
        }
        return _ff
    else:
        return {}


# 对2种过程，分别创建 Impl 对象，并分别记录在对应过程的 FormFactor 对象内。
for process in ['B->pi', 'Bs->K']:
    impl = Impl(
        'z-param by 1501.05373',  # Impl 本身不依赖过程，所以名字中不必体现过程
        ff_obj=formfactors[process],  # 便于逆向找到所属的过程
        ff_names=['f+', 'f0'],
        param_form='z-param',
        methods='LQCD',
        ref='arXiv：1501.05373 [hep-lat]')
    impl.set_description = (f"用{impl.param_form}参数化和{impl.methods}方法，"
                            f"实现了{impl.ff_names}，参考了{impl.ref}")
    impl.set_func(lambda qsq: ff(process, qsq))
    formfactors[process].add_impl(impl)  # 将 Impl 注册进 FormFactor 对象
