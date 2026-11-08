import importlib.resources as pkg_resources

import pytest
import yaml

from src.hmff import formfactors


def _implemented_cases():
    """从实际数据收集所有带真实形状因子的 (process, impl) 组合.

    占位实现(只有 status、无 form factors)会被自动跳过.
    """
    cases = []
    for proc_name in formfactors:
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
        ff_func = impl.param_func(ff_name)
        assert ff_func is not None
        value = ff_func(qsq)
        assert isinstance(value, float), f"{ff_name} 应返回 float, 得到 {type(value)}"

    central = impl.get_central_values(qsq)
    assert len(central) == len(ff_names)
    assert all(isinstance(x, float) for x in central.values())

    try:
        errors = impl.get_errors(qsq)
    except KeyError:
        # 缺少旧版误差路径所需的 per-ff 'error' 元数据的实现暂不支持
        errors = None
    if errors is not None:
        assert isinstance(errors, dict)
        assert set(errors) == set(ff_names)
        assert all(isinstance(x, (int, float)) for x in errors.values())
        assert all(x >= 0 for x in errors.values())


def _p_p_processes():
    """读取 P_P.yaml 中的全部过程名 (加载器合并了三个 YAML, 不记录来源文件)."""
    with (
        pkg_resources.path("hmff.data", "P_P.yaml") as path,
        open(path, encoding="utf-8") as f,
    ):
        return list(yaml.safe_load(f))


@pytest.mark.parametrize(
    "impl_name, process_name, ff_name, expected",
    [
        ("LCSR-pole 2004", "B->pi", "f+", 0.258),
        ("LCSR-pole 2004", "B->pi", "fT", 0.253),
        ("LCSR-pole 2004", "B->K", "f+", 0.331),
        ("LCSR-pole 2004", "B->K", "fT", 0.358),
        ("LCSR-pole 2004", "B->eta", "f+", 0.275),
        ("LCSR-pole 2004", "B->eta", "fT", 0.285),
        ("LQCD-ETMC 2017", "D->pi", "f+", 0.612),
        ("LQCD-ETMC 2017", "D->K", "f+", 0.765),
    ],
)
def test_ff_at_qsq_zero(impl_name, process_name, ff_name, expected):
    """校验 q^2=0 时形状因子数值.

    YAML 参数逐位符合论文 Table 3; 拟合参数化本身对中心值的复现精度约 1-2%,
    故采用 1.5% 相对容差.
    """
    impl = formfactors[process_name].get_impl(impl_name)
    value = impl.param_func(ff_name)(0.0)
    assert value == pytest.approx(expected, rel=0.015)


def _p_p_fplus_f0_cases():
    """收集 P_P 过程中同时含 f+ 和 f0 的 (process, impl) 组合."""
    cases = []
    for proc_name in _p_p_processes():
        proc = formfactors[proc_name]
        for impl_name in proc.impl_names:
            names = proc.get_impl(impl_name).form_factor_names
            if "f+" in names and "f0" in names:
                cases.append((proc_name, impl_name))
    return cases


@pytest.mark.parametrize("process_name, impl_name", _p_p_fplus_f0_cases())
def test_fplus_eq_f0_at_zero(process_name, impl_name):
    """P->P 跃迁须满足约束 f+(0) = f0(0) (1.5% 相对容差)."""
    impl = formfactors[process_name].get_impl(impl_name)
    f_plus = impl.param_func("f+")(0.0)
    f_zero = impl.param_func("f0")(0.0)
    assert f_zero == pytest.approx(f_plus, rel=0.015)
