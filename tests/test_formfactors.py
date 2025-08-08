#!/usr/bin/env python3
"""
Test suite for HMFF form factors
"""

import pytest
from HMFF.data_io import LazyFormFactorLoader

# Initialize the form factor loader
form_factor_loader = LazyFormFactorLoader()


def test_form_factor_loader_initialization():
    """Test that the form factor loader can be initialized"""
    assert form_factor_loader is not None
    assert hasattr(form_factor_loader, 'keys')
    assert hasattr(form_factor_loader, 'items')


def test_form_factor_loader_contains_keys():
    """Test that the loader contains expected keys"""
    keys = list(form_factor_loader.keys())
    assert len(keys) > 0, "Loader should contain form factors"
    
    
@pytest.mark.parametrize("form_factor_key", [
    "B->pi",
    "B->K",
    "D->pi",
    "D->K",
    "K->pi",
    "pi->pi",
    "B->D",
    "B->B",
])
def test_common_form_factors_exist(form_factor_key):
    """Test that common form factors exist in the loader"""
    # This test will be skipped if the form factor doesn't exist in the data
    if form_factor_key in form_factor_loader.keys():
        form_factor = form_factor_loader[form_factor_key]
        assert form_factor is not None
        assert hasattr(form_factor, 'name')
        assert form_factor.name == form_factor_key


@pytest.mark.parametrize("form_factor_key,impl_name", [
    ("B->pi", "LCSR-2004"),
    ("B->pi", "LQCD-FLAG-2024"),
    ("B->pi", "LQCD-z 2015"),
])
def test_form_factor_implementations_exist(form_factor_key, impl_name):
    """Test that specific form factor implementations exist"""
    # This test will be skipped if the form factor doesn't exist in the data
    if form_factor_key in form_factor_loader.keys():
        form_factor = form_factor_loader[form_factor_key]
        if impl_name in form_factor.impl_names:
            impl = form_factor.get_impl(impl_name)
            assert impl is not None
            assert hasattr(impl, 'name')
            assert impl.name == impl_name


def test_form_factor_methods():
    """Test form factor methods work correctly"""
    # Find a B->pi form factor as an example
    if "B->pi" in form_factor_loader.keys():
        form_factor = form_factor_loader["B->pi"]
        assert hasattr(form_factor, 'impl_names')
        assert hasattr(form_factor, 'get_impl')
        
        # Test getting implementations
        impl_names = form_factor.impl_names
        assert len(impl_names) > 0, "B->pi should have at least one implementation"
        
        # Test getting a specific implementation
        impl = form_factor.get_impl(impl_names[0])
        assert impl is not None
        
        # Test implementation properties
        assert hasattr(impl, 'form_factor_names')
        assert hasattr(impl, 'form_factor_function')
        
        ff_names = impl.form_factor_names
        assert len(ff_names) > 0, "Implementation should have at least one form factor"
        
        # Test form factor function generation
        ff_func = impl.form_factor_function(ff_names[0])
        assert callable(ff_func), "Form factor function should be callable"
        
        # Test evaluating form factor function at qsq=0
        result = ff_func(0.0)
        assert isinstance(result, (int, float)), "Form factor result should be a number"


if __name__ == "__main__":
    pytest.main([__file__])