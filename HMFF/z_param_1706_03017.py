"""参考1706.03017 [hep-lat]"""
import math
import yaml
import codecs
from pathlib import Path
from .classes import Impl
from .initialization import formfactors

# 定义初始值
m1 = {'D': 1.87265}
m2 = {'pi': 0.134977, 'K': 0.495644}
mDstar = 2.1122

# 从文件中加载参数
with codecs.open(Path(__file__).parent / 'data/Lubicz_Riggio.yaml', 'r', encoding='utf-8') as file:
    ff_pars = yaml.load(file, yaml.SafeLoader)


def z(q2, IS, FS):
    # ref: eq.39
    tp = (m1.get(IS) + m2.get(FS))**2
    t0 = (m1.get(IS) + m2.get(FS)) * (math.sqrt(m1.get(IS)) - math.sqrt(m2.get(FS)))**2
    return (math.sqrt(tp - q2) - math.sqrt(tp - t0)) / (math.sqrt(tp - q2) + math.sqrt(tp - t0))


def fpi(IS, FS, qs, pars):
    # ref: eq.68
    f0 = pars['f(0)']
    cp = pars['cp']
    pv = pars['PV']
    return (f0 + cp * (z(qs, IS, FS) - z(0, IS, FS)) *
            (1 + (z(qs, IS, FS) + z(0, IS, FS)) / 2)) / (1 - pv * qs**2)


def f0i(IS, FS, qs, pars):
    # ref: eq.69
    f0 = pars['f(0)']
    c0 = pars['c0']
    ps = pars['PS']
    return (f0 + c0 * (z(qs, IS, FS) - z(0, IS, FS)) *
            (1 + (z(qs, IS, FS) + z(0, IS, FS)) / 2)) / (1 - ps * qs**2)


def fp(IS, FS, qs, pars):
    # ref: eq.70
    f0 = pars['f(0)']
    cp = pars['cp']
    return (f0 + cp * (z(qs, IS, FS) - z(0, IS, FS)) *
            (1 + (z(qs, IS, FS) + z(0, IS, FS)) / 2)) / (1 - qs / mDstar**2)


def f0(IS, FS, qs, pars):
    # ref eq.71
    f0 = pars['f(0)']
    c0 = pars['c0']
    return (f0 + c0 * (z(qs, IS, FS) - z(0, IS, FS)) * (1 + (z(qs, IS, FS) + z(0, IS, FS)) / 2))


def ff(process, q2):
    parts = process.split('->')
    IS = parts[0]
    FS = parts[1]
    if 'D->pi' in process:
        _ff = {
            'f+': fpi(IS, FS, q2, pars=ff_pars[process + ' form factor']),
            'f0': f0i(IS, FS, q2, pars=ff_pars[process + ' form factor']),
        }
        return _ff
    elif 'D->K' in process:
        _ff = {
            'f+': fp(IS, FS, q2, pars=ff_pars[process + ' form factor']),
            'f0': f0(IS, FS, q2, pars=ff_pars[process + ' form factor']),
        }
        return _ff
    else:
        return {}


# 对2种过程，分别创建 Impl 对象，并分别记录在对应过程的 FormFactor 对象内。
for process in ['D->K', 'D->pi']:
    impl = Impl(
        'z-param by 1706.03017',  # Impl 本身不依赖过程，所以名字中不必体现过程
        ff_obj=formfactors[process],  # 便于逆向找到所属的过程
        ff_names=['f+', 'f0'],
        param_form='z-param',
        methods='LQCD',
        ref='arXiv：1706.03017 [hep-lat]')
    impl.set_description = (f"用{impl.param_form}参数化和{impl.methods}方法，"
                            f"实现了{impl.ff_names}，参考了{impl.ref}")
    impl.set_func(lambda qsq: ff(process, qsq))
    formfactors[process].add_impl(impl)  # 将 Impl 注册进 FormFactor 对象
