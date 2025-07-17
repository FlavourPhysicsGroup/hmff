"""初始化，实现一些基本信息。"""
from .classes import FormFactor

formfactors = {}  # 存储实现对象的字典, e.g. {name: obj_ff} 其中 obj_ff 是 FormFactor 类的对象 (object)

# B->D
all_ff = ['f+', 'f0', 'fT']
formfactors['B->D'] = FormFactor('B', 'D', ff_names=all_ff)

# B->P: 此类过程共有三种形状因子
all_ff = ['f+', 'f0', 'fT']
formfactors['B->K'] = FormFactor('B', 'K', ff_names=all_ff)
formfactors['B->pi'] = FormFactor('B', 'pi', ff_names=all_ff)
formfactors['B->eta'] = FormFactor('B', 'eta', ff_names=all_ff)

# B->V
all_ff = ['V', 'A0', 'A1', 'A2', 'T1', 'T2', 'T3']
formfactors['B->K*'] = FormFactor('B', 'K*', ff_names=all_ff)
formfactors['B->rho'] = FormFactor('B', 'rho', ff_names=all_ff)
formfactors['B->omega'] = FormFactor('B', 'omega', ff_names=all_ff)

# Bs->P
all_ff = ['f+', 'f0', 'fT']
formfactors['Bs->K'] = FormFactor('Bs', 'K', ff_names=all_ff)

# Bs->V
all_ff = ['V', 'A0', 'A1', 'A2', 'T1', 'T2', 'T3']
formfactors['Bs->K*'] = FormFactor('Bs', 'K*', ff_names=all_ff)
formfactors['Bs->phi'] = FormFactor('Bs', 'phi', ff_names=all_ff)

# D->P
all_ff = ['f+', 'f0', 'fT']
formfactors['D->K'] = FormFactor('D', 'K', ff_names=all_ff)
formfactors['D->pi'] = FormFactor('D', 'pi', ff_names=all_ff)
