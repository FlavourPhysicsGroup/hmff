#!/usr/bin/env python3
"""
HMFF 数据加载器与 process/impl 元数据测试.

形状因子的数值求值测试见 test_impls.py; 本文件聚焦
LazyFormFactorLoader 的行为与每个 process/impl 元数据的完整性.
"""

import pytest
from src.hmff.data_io import LazyFormFactorLoader

# 全局加载器
form_factor_loader = LazyFormFactorLoader()


def test_loader_initialization():
    """加载器可初始化"""
    assert form_factor_loader is not None
    assert hasattr(form_factor_loader, "keys")
    assert hasattr(form_factor_loader, "items")


def test_loader_contains_keys():
    """加载器包含数据"""
    assert len(list(form_factor_loader.keys())) > 0


def test_loader_is_lazy():
    """加载器是懒加载的"""
    loader = LazyFormFactorLoader()
    assert loader._cache is None
    _ = list(loader.keys())
    assert loader._cache is not None


@pytest.mark.parametrize("form_factor_key", sorted(form_factor_loader.keys()))
def test_form_factor_meta(form_factor_key):
    """每个 process 的名称/初末态/实现列表完整"""
    ff = form_factor_loader[form_factor_key]
    assert ff.name == form_factor_key
    assert hasattr(ff, "IS") and hasattr(ff, "FS")
    assert isinstance(ff.impl_configs, dict)
    assert isinstance(ff.impl_names, list) and ff.impl_names


@pytest.mark.parametrize("form_factor_key", sorted(form_factor_loader.keys()))
def test_impl_meta(form_factor_key):
    """每个实现的元数据属性存在(占位实现可缺 form factors)"""
    ff = form_factor_loader[form_factor_key]
    for impl_name in ff.impl_names:
        impl = ff.get_impl(impl_name)
        assert impl.name == impl_name
        assert isinstance(impl.config, dict)
        for prop in ("ref", "method", "citation", "comment", "form_factor_names"):
            assert hasattr(impl, prop), f"{form_factor_key}/{impl_name} 缺 {prop}"
        if impl.form_factor_names:
            ffs = impl.config.get("form factors")
            assert isinstance(ffs, dict) and ffs


def test_get_central_values_returns_numbers():
    """对有真实形状因子的实现, get_central_values 返回等长数字列表"""
    for proc_name in form_factor_loader.keys():
        ff = form_factor_loader[proc_name]
        for impl_name in ff.impl_names:
            impl = ff.get_impl(impl_name)
            if not impl.form_factor_names:
                continue
            vals = impl.get_central_values(1.0)
            assert isinstance(vals, list)
            assert len(vals) == len(impl.form_factor_names)
            assert all(isinstance(v, (int, float)) for v in vals)


def test_error_handling():
    """错误处理: 不存在的实现/形状因子抛 KeyError"""
    proc = form_factor_loader[sorted(form_factor_loader.keys())[0]]
    with pytest.raises(KeyError):
        proc.get_impl("NonExistentImpl")
    impl = proc.get_impl(proc.impl_names[0])
    with pytest.raises(KeyError):
        impl.form_factor_function("NonExistentFF")


if __name__ == "__main__":
    pytest.main([__file__])
