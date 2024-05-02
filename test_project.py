# %%
import HMFF
from HMFF.classes import FormFactor, Impl

# %%
print(HMFF.formfactors.keys())

# %%
ff_bk: FormFactor = HMFF.formfactors['B->K']

print(ff_bk.impl_names)

# %%
ff_bk_impl: Impl = ff_bk.get_impl('one-pole by 0406232')
print(ff_bk_impl.get_central_values(qsq=2.0))

# %%
ff_bk_impl.draw(14, 1)
# %%
