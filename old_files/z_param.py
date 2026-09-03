import math
import yaml
import codecs
from pathlib import Path
# 定义初始值
ap = [0.0, 0.0, 0.0]
mB = {'B': 5.27966, 'D': 1.87265, 'Bs': 5.36692}
mD = {'pi': 0.134977, 'D': 1.86966, 'K': 0.495644}
mBstar = {'B->pi': 5.3252, 'B->D': 6.329, 'D->K': 2.1122, 'Bs->K': 5.3252, 'B->K': 5.4}
mB0star = {'Bs->K': 5.63}
# 从文件中加载参数
with codecs.open(Path(__file__).parent / 'data/z_param.yaml', 'r', encoding='utf-8') as file:
    ff_pars = yaml.load(file, yaml.SafeLoader)


# 计算z函数
def z(q2, IS, FS):
    tp = (mB.get(IS) + mD.get(FS))**2
    t0 = (mB.get(IS) + mD.get(FS)) * (math.sqrt(mB.get(IS)) - math.sqrt(mD.get(FS)))**2
    return (math.sqrt(tp - q2) - math.sqrt(tp - t0)) / (math.sqrt(tp - q2) + math.sqrt(tp - t0))

# 不同拟合方法
def z1(q2, IS, FS):
    tp = (mB.get(IS) + mD.get(FS))**2
    tm = (mB.get(IS) - mD.get(FS))**2
    t0 = tp - math.sqrt(tp * (tp - tm))
    return (math.sqrt(tp - q2) - math.sqrt(tp - t0)) / (math.sqrt(tp - q2) + math.sqrt(tp - t0))

# 计算BCL表示的f+或fT
def fpBCL(IS, FS, q2, pars):
    ap = pars
    result = 0
    key = IS + '->' + FS
    for n in range(0, 3):
        term = (z(q2, IS, FS)**n - (-1)**(n - 3) * n / 3 * z(q2, IS, FS)**3) * ap[n]
        result += term
    return 1 / (1 - q2 / mBstar.get(key)**2) * result


# 计算BCL表示的f0
def f0BCL(IS, FS, q2, pars):
    a0 = pars
    result = 0
    for n in range(0, 3):
        term = a0[n] * z(q2, IS, FS)**n
        result += term
    return result

# 不同拟合方法
def f0BCL1(IS, FS, q2, pars):
    a0 = pars
    key = IS + '->' + FS
    result = 0
    for n in range(0, 3):
        term = a0[n] * z1(q2, IS, FS)**n
        result += term
    return 1 / (1 - q2 / mB0star.get(key)**2) * result


def fp(IS, FS, qs, pars):
    key = IS + '->' + FS
    f0 = pars['f(0)']
    cp = pars['cp']
    return (f0 + cp * (z(qs, IS, FS) - z(0, IS, FS)) *
            (1 + (z(qs, IS, FS) + z(0, IS, FS)) / 2)) / (1 - qs / mBstar.get(key)**2)


def f0(IS, FS, qs, pars):
    f0 = pars['f(0)']
    c0 = pars['c0']
    return (f0 + c0 * (z(qs, IS, FS) - z(0, IS, FS)) * (1 + (z(qs, IS, FS) + z(0, IS, FS)) / 2))


def fpi(IS, FS, qs, pars):
    f0 = pars['f(0)']
    cp = pars['cp']
    pv = pars['PV']
    return (f0 + cp * (z(qs, IS, FS) - z(0, IS, FS)) *
            (1 + (z(qs, IS, FS) + z(0, IS, FS)) / 2)) / (1 - pv * qs**2)


def f0i(IS, FS, qs, pars):
    f0 = pars['f(0)']
    c0 = pars['c0']
    ps = pars['PS']
    return (f0 + c0 * (z(qs, IS, FS) - z(0, IS, FS)) *
            (1 + (z(qs, IS, FS) + z(0, IS, FS)) / 2)) / (1 - ps * qs**2)


# 选择所需参数并代入计算，最后输出字典
def ff(IS, FS, q2):
    key = IS + '->' + FS
    if 'B->pi' in key:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['ap']),
            'f0': f0BCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['a0']),
            'fT': fpBCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['aT'])
        }
        return _ff
    elif 'B->D' in key:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['ap']),
            'f0': f0BCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['a0']),
        }
        return _ff
    elif 'D->K' in key:
        _ff = {
            'f+': fp(IS, FS, q2, pars=ff_pars[key + ' form factor']),
            'f0': f0(IS, FS, q2, pars=ff_pars[key + ' form factor']),
        }
        return _ff
    elif 'D->pi' in key:
        _ff = {
            'f+': fpi(IS, FS, q2, pars=ff_pars[key + ' form factor']),
            'f0': f0i(IS, FS, q2, pars=ff_pars[key + ' form factor']),
        }
        return _ff
    elif 'Bs->K' in key:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['ap']),
            'f0': f0BCL1(IS, FS, q2, pars=ff_pars[key + ' form factor']['a0']),
        }
        return _ff
    elif 'B->K' in key:
        _ff = {
            'f+': fpBCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['ap']),
            'f0': f0BCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['a0']),
            'fT': fpBCL(IS, FS, q2, pars=ff_pars[key + ' form factor']['aT'])
        }
        return _ff
    else:
        return {}
