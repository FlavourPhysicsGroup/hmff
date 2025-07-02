import codecs
from pathlib import Path
import yaml

with codecs.open(Path(__file__).parent / 'data/one_pole.yaml', 'r', encoding='utf-8') as file:
    ff_pars = yaml.load(file, yaml.SafeLoader)


def fp_pi(q2, pars):
    r1 = pars.get('r1')
    r2 = pars.get('r2')
    m12 = pars.get('m1')**2
    mfit2 = pars.get('mfit^2')
    return r1 / (1 - q2 / m12) + r2 / (1 - q2 / mfit2)


def fp_K(q2, pars):
    r1 = pars.get('r1')
    r2 = pars.get('r2')
    m12 = pars.get('m1')**2
    return r1 / (1 - q2 / m12) + r2 / (1 - q2 / m12)**2


def f0(q2, pars):
    r2 = pars.get('r2')
    mfit2 = pars.get('mfit^2')
    return r2 / (1 - q2 / mfit2)


def f_eq59(q2, pars):
    r1 = pars.get('r1')
    r2 = pars.get('r2')
    m12 = pars.get('mR')**2
    mfit2 = pars.get('mfit^2')
    return r1 / (1 - q2 / m12) + r2 / (1 - q2 / mfit2)


def f_eq60(q2, pars):
    r1 = pars.get('r1')
    r2 = pars.get('r2')
    mfit2 = pars.get('mfit^2')
    return r1 / (1 - q2 / mfit2) + r2 / (1 - q2 / mfit2)**2


def f_eq61(q2, pars):
    r2 = pars.get('r2')
    mfit2 = pars.get('mfit^2')
    return r2 / (1 - q2 / mfit2)


def ff(IS, FS, q2):
    key = IS + '->' + FS
    _processes = ['B->rho', 'Bs->K*', 'B->K*', 'B->omega', 'Bs->phi']
    if 'B->pi' in key:
        _ff = {
            'f+': fp_pi(q2, pars=ff_pars[key + ' form factor']['f+']),
            'f0': f0(q2, pars=ff_pars[key + ' form factor']['f0']),
            'fT': fp_pi(q2, pars=ff_pars[key + ' form factor']['fT'])
        }
        return _ff
    elif 'B->K' in key:
        _ff = {
            'f+': fp_K(q2, pars=ff_pars[key + ' form factor']['f+']),
            'f0': f0(q2, pars=ff_pars[key + ' form factor']['f0']),
            'fT': fp_K(q2, pars=ff_pars[key + ' form factor']['fT'])
        }
        return _ff
    elif 'B->eta' in key:
        _ff = {
            'f+': fp_K(q2, pars=ff_pars[key + ' form factor']['f+']),
            'f0': f0(q2, pars=ff_pars[key + ' form factor']['f0']),
            'fT': fp_K(q2, pars=ff_pars[key + ' form factor']['fT'])
        }
        return _ff
    elif key in _processes:
        _ff = {
            'V': f_eq59(q2, pars=ff_pars[key + ' form factor']['V']),
            'A0': f_eq59(q2, pars=ff_pars[key + ' form factor']['A0']),
            'A1': f_eq61(q2, pars=ff_pars[key + ' form factor']['A1']),
            'A2': f_eq60(q2, pars=ff_pars[key + ' form factor']['A2']),
            'T1': f_eq59(q2, pars=ff_pars[key + ' form factor']['T1']),
            'T2': f_eq61(q2, pars=ff_pars[key + ' form factor']['T2']),
            'T3': f_eq60(q2, pars=ff_pars[key + ' form factor']['T3'])
        }
        return _ff
    else:
        return {}
