#!/usr/bin/env python

"""B介子衰变到赝标介子过程的形状因子, 参考hep-ph/0406232"""

from .classes import Impl
from .initialization import formfactors
from functools import partial
from pathlib import Path
import yaml

with open(Path(__file__).parent / 'data/ball_zwicky.yaml', 'r', encoding='utf-8') as file:
    ff_pars = yaml.load(file, yaml.SafeLoader)


def fp_pi(q2, pars):
    r1 = pars.get('r1')
    r2 = pars.get('r2')
    m12 = pars.get('m1') ** 2
    mfit2 = pars.get('mfit^2')
    return r1 / (1 - q2 / m12) + r2 / (1 - q2 / mfit2)


def fp_K(q2, pars):
    r1 = pars.get('r1')
    r2 = pars.get('r2')
    m12 = pars.get('m1') ** 2
    return r1 / (1 - q2 / m12) + r2 / (1 - q2 / m12) ** 2


def f0(q2, pars):
    r2 = pars.get('r2')
    mfit2 = pars.get('mfit^2')
    return r2 / (1 - q2 / mfit2)


def ff(process, qsq):
    if 'B->pi' in process:
        _ff = {'f+': fp_pi(qsq, pars=ff_pars['B->pi form factor']['f+']),
               'f0': f0(qsq, pars=ff_pars['B->pi form factor']['f0']),
               'fT': fp_pi(qsq, pars=ff_pars['B->pi form factor']['fT'])}
        return _ff
    elif 'B->K' in process:
        _ff = {'f+': fp_K(qsq, pars=ff_pars['B->K form factor']['f+']),
               'f0': f0(qsq, pars=ff_pars['B->K form factor']['f0']),
               'fT': fp_K(qsq, pars=ff_pars['B->K form factor']['fT'])}
        return _ff
    elif 'B->eta' in process:
        _ff = {'f+': fp_K(qsq, pars=ff_pars['B->eta form factor']['f+']),
               'f0': f0(qsq, pars=ff_pars['B->eta form factor']['f0']),
               'fT': fp_K(qsq, pars=ff_pars['B->eta form factor']['fT'])}
        return _ff
    else:
        return {}


# 对三种过程，分别创建 Impl 对象，并分别记录在对应过程的 FormFactor 对象内。
for process in ['B->pi', 'B->K', 'B->eta']:
    impl = Impl(
        'one-pole by 0406232',  # Impl 本身不依赖过程，所以名字中不必体现过程
        ff_obj=formfactors[process],  # 便于逆向找到所属的过程
        ff_names=['f+', 'f0', 'fT'],
        param_form='one-pole',
        methods='LCSR',
        ref='arxiv:hep-ph/0406232')
    impl.set_description = (f"用{impl.param_form}参数化和{impl.methods}方法，"
                            f"实现了{impl.ff_names}，参考了{impl.ref}")
    impl.set_func(partial(ff, process))
    formfactors[process].add_impl(impl)     # 将 Impl 注册进 FormFactor 对象
