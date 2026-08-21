import pytest
from HMFF import formfactors


@pytest.mark.parametrize("ff_name, impl_name", [
    ("Lambda_b->Lambda", "LQCD-2016-nominal"),
    ("Lambda_b->Lambda", "LQCD-2016-HO"),
    ("Lambda_b->Lambda", "LQCD-2016"),
    ("Lambda_b->Lambda_1520", "LQCD-2021-nominal"),
    ("Lambda_b->Lambda_1520", "LQCD-2021-HO"),
    ("Lambda_b->Lambda_1520", "LQCD-2021"),
    ("Lambda_b->Lambda_1520", "LCSR-2024"),
    ("B->pi", "LCSR-pole 2004"),
    ("B->pi", "LQCD-FLAG-2024"),
    ("B->pi", "LQCD-z 2015"),
    ("B->K", "LCSR-pole 2004"),
    ("B->K", "LQCD-FLAG-2024"),
    ("B->eta", "LCSR-pole 2004"),
    ("Bs->K", "LQCD-z 2015"),
    ("Bs->K", "LQCD-FLAG-2024"),
    ("B->D", "LQCD-FLAG-2024"),
    ("D->pi", "LQCD-z 2017"),
    ("D->K", "LQCD-z 2017"),
    ("B->rho", "LQCD-2008"),
    ("B->rho", "LCSR-pole"),
    ("B->K*", "LQCD-2015"),
    ("B->K*", "LCSR-pole"),
    ("B->omega", "LCSR-pole"),
    ("Bs->K*", "LQCD-2015"),
    ("Bs->K*", "LCSR-pole"),
    ("Bs->phi", "LQCD-2015"),
    ("Bs->phi", "LCSR-pole"),
])
def test_impls(ff_name, impl_name):
    qsq = 1
    ff = formfactors[ff_name]
    impl = ff.get_impl(impl_name)
    assert ff is not None
    assert impl is not None
    # UNFINISHED 实现或尚无 form factors 的实现不参与数值测试
    if impl.config.get("status") == "UNFINISHED" or not impl.form_factor_names:
        pytest.skip(f"Impl '{impl_name}' of '{ff_name}' is UNFINISHED")
    all_ff_names = impl.form_factor_names
    for ff_name in all_ff_names:
        ff_func = impl.form_factor_function(ff_name)
        assert ff_func is not None
        ff_val = ff_func(qsq)
        assert isinstance(ff_val, float)

    all_ff_vals = impl.get_central_values(qsq)
    assert len(all_ff_vals) == len(all_ff_names)
    assert all([isinstance(x, float) for x in all_ff_vals])