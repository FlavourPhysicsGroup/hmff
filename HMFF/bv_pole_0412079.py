#!/usr/bin/env python

"""B介子衰变到矢量介子定义, 参考hep-ph/0412079"""
from .classes import Impl
from .initialization import formfactors
from functools import partial
from pathlib import Path
import yaml

with open(Path(__file__).parent / 'data/ball_zwicky.yaml', 'r') as file:
    ff_pars = yaml.load(file, yaml.SafeLoader)


def f_eq59(q2, pars):
    r1 = pars.get('r1')
    r2 = pars.get('r2')
    m12 = pars.get('mR') ** 2
    mfit2 = pars.get('mfit^2')
    return r1 / (1 - q2 / m12) + r2 / (1 - q2 / mfit2)


def f_eq60(q2, pars):
    r1 = pars.get('r1')
    r2 = pars.get('r2')
    mfit2 = pars.get('mfit^2')
    return r1 / (1 - q2 / mfit2) + r2 / (1 - q2 / mfit2) ** 2


def f_eq61(q2, pars):
    r2 = pars.get('r2')
    mfit2 = pars.get('mfit^2')
    return r2 / (1 - q2 / mfit2)


def ff(process, q2):
    _processes = ['B->rho', 'Bs->K*', 'B->K*', 'B->omega', 'Bs->phi']
    if process in _processes:
        _ff = {'V': f_eq59(q2, pars=ff_pars[process + ' form factor']['V']),
               'A0': f_eq59(q2, pars=ff_pars[process + ' form factor']['A0']),
               'A1': f_eq61(q2, pars=ff_pars[process + ' form factor']['A1']),
               'A2': f_eq60(q2, pars=ff_pars[process + ' form factor']['A2']),
               'T1': f_eq59(q2, pars=ff_pars[process + ' form factor']['T1']),
               'T2': f_eq61(q2, pars=ff_pars[process + ' form factor']['T2']),
               'T3': f_eq60(q2, pars=ff_pars[process + ' form factor']['T3'])}
        # _ff['T3_notilde_nomass'] = (_ff['T3'] - _ff['T2']) / q2
        return _ff
    else:
        return {}


# 对六种过程，分别创建 Impl 对象，并分别记录在对应过程的 FormFactor 对象内。
for process in ['B->rho', 'Bs->K*', 'B->K*', 'B->omega', 'Bs->phi']:
    impl = Impl(
        'one-pole by 0412079',  # Impl 本身不依赖过程，所以名字中不必体现过程
        ff_obj=formfactors[process],  # 便于逆向找到所属的过程
        ff_names=['V', 'A0', 'A1', 'A2', 'T1', 'T2', 'T3'],
        param_form='one-pole',
        methods='LCSR',
        ref='arxiv:hep-ph/0412079')
    impl.set_description = (f"用{impl.param_form}参数化和{impl.methods}方法，"
                            f"实现了{impl.ff_names}，参考了{impl.ref}")
    impl.set_func(partial(ff, process))
    formfactors[process].add_impl(impl)     # 将 Impl 注册进 FormFactor 对象
