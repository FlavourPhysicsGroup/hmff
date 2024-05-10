# %%
import HMFF
from HMFF.classes import FormFactor, Impl

# %%
# HMFF.formfactors 这个字典内包含所有已经实现的过程：{'过程名'：形状因子对象}
print(HMFF.formfactors.keys())

# %%
# 取出 B->K 过程形状因子的对象，赋值给 ff_bk. 此时 ff_bk 对象内包含着 B->K 过程形状因子的所有信息
ff_bk: FormFactor = HMFF.formfactors['B->K']

# 查看 B->K 过程形状因子有多少种实现方法
print(ff_bk.impl_names)

# %%
# 取出 B->K 过程形状因子的一种实现方式，赋值给 ff_bk_impl. 
# 此时可以从 ff_bk_impl 对象获取 B->K 过程形状因子对应不同 q2 时的具体数值
ff_bk_impl: Impl = ff_bk.get_impl('one-pole by 0406232')
print(ff_bk_impl.get_central_values(qsq=2.0))

# %%
# 这个方法是多余的，但既然你们实现了，就可以用这种方式调用。
ff_bk_impl.draw(14, 1)
# %%
