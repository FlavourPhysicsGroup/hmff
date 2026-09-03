import pytest
from src.hmff import formfactors


def _implemented_cases():
    """从实际数据收集所有带真实形状因子的 (process, impl) 组合.

    占位实现(只有 status、无 form factors)会被自动跳过.
    """
    cases = []
    for proc_name in formfactors.keys():
        proc = formfactors[proc_name]
        for impl_name in proc.impl_names:
            if proc.get_impl(impl_name).form_factor_names:
                cases.append((proc_name, impl_name))
    return cases


@pytest.mark.parametrize("process_name, impl_name", _implemented_cases())
def test_impl_values(process_name, impl_name):
    """每个已实现形状因子都能在 qsq=1 处求值并返回 float."""
    qsq = 1.0
    impl = formfactors[process_name].get_impl(impl_name)
    ff_names = impl.form_factor_names
    assert ff_names

    for ff_name in ff_names:
        ff_func = impl.form_factor_function(ff_name)
        assert ff_func is not None
        value = ff_func(qsq)
        assert isinstance(value, float), f"{ff_name} 应返回 float, 得到 {type(value)}"

    central = impl.get_central_values(qsq)
    assert len(central) == len(ff_names)
    assert all(isinstance(x, float) for x in central)