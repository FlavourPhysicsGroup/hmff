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


def test_form_factor_loader_is_lazy():
    """Test that the loader is actually lazy - data is loaded only when accessed"""
    # Create a new loader to test lazy loading
    loader = LazyFormFactorLoader()
    # At this point, no data should be loaded yet
    assert loader._cache is None
    # Accessing keys should trigger loading
    _ = list(loader.keys())
    # Cache should now be populated
    assert loader._cache is not None


@pytest.mark.parametrize("form_factor_key", [
    "B->pi",
    "B->K", 
    "B->eta",
    "Bs->K",
    "B->D",
    "D->pi",
    "D->K",
    "B->rho",
    "B->K*",
    "B->omega",
    "Bs->K*",
    "Bs->phi",
    "Lambda_b->Lambda",
    "Lambda_b->Lambda_1520"
])
def test_common_form_factors_exist(form_factor_key):
    """Test that common form factors exist in the loader"""
    # This test will be skipped if the form factor doesn't exist in the data
    if form_factor_key in form_factor_loader.keys():
        form_factor = form_factor_loader[form_factor_key]
        assert form_factor is not None
        assert hasattr(form_factor, 'name')
        assert form_factor.name == form_factor_key
        # Test that form factors have initial and final state names
        assert hasattr(form_factor, 'IS')  # Initial state
        assert hasattr(form_factor, 'FS')  # Final state
        
        # Test that form factors have implementation configs
        assert hasattr(form_factor, 'impl_configs')
        assert isinstance(form_factor.impl_configs, dict)
        
        # Test that form factors have implementation names
        assert hasattr(form_factor, 'impl_names')
        assert isinstance(form_factor.impl_names, list)


@pytest.mark.parametrize("form_factor_key,expected_impl_count", [
    ("B->pi", 3),      # LCSR-2004, LQCD-FLAG-2024, LQCD-z 2015
    ("B->K", 2),       # LCSR-2004, LQCD-FLAG-2024
    ("Bs->K", 2),      # LQCD-z 2015, LQCD-FLAG-2024
    ("B->eta", 1),     # LCSR-pole 2004
    ("B->D", 1),       # LQCD-FLAG-2024
    ("D->pi", 1),      # LQCD-z 2017
    ("D->K", 1),       # LQCD-z 2017
    ("Lambda_b->Lambda", 2),     # LQCD-2016-nominal, LQCD-2016-HO
    ("Lambda_b->Lambda_1520", 2), # LQCD-2021-nominal, LQCD-2021-HO
    ("B->rho", 1),     # LCSR-pole
    ("B->K*", 2),      # LQCD-2015, LCSR-pole
    ("B->omega", 1),   # LCSR-pole
    ("Bs->K*", 2),     # LQCD-2015, LCSR-pole
    ("Bs->phi", 2),    # LQCD-2015, LCSR-pole
])
def test_form_factor_impl_count(form_factor_key, expected_impl_count):
    """Test that form factors have the expected number of implementations"""
    if form_factor_key in form_factor_loader.keys():
        form_factor = form_factor_loader[form_factor_key]
        assert len(form_factor.impl_names) >= expected_impl_count, \
            f"{form_factor_key} should have at least {expected_impl_count} implementations"


@pytest.mark.parametrize("form_factor_key,impl_name", [
    ("B->pi", "LCSR-2004"),
    ("B->pi", "LQCD-FLAG-2024"),
    ("B->pi", "LQCD-z 2015"),
    ("B->K", "LCSR-2004"),
    ("B->K", "LQCD-FLAG-2024"),
    ("D->pi", "LQCD-z 2017"),
    ("D->K", "LQCD-z 2017"),
    ("Bs->K", "LQCD-z 2015"),
    ("Bs->K", "LQCD-FLAG-2024"),
    ("B->eta", "LCSR-pole 2004"),
    ("B->D", "LQCD-FLAG-2024"),
    ("Lambda_b->Lambda", "LQCD-2016-nominal"),
    ("Lambda_b->Lambda", "LQCD-2016-HO"),
    ("Lambda_b->Lambda_1520", "LQCD-2021-nominal"),
    ("Lambda_b->Lambda_1520", "LQCD-2021-HO"),
    ("B->rho", "LCSR-pole"),
    ("B->K*", "LCSR-pole"),
    ("B->omega", "LCSR-pole"),
    ("Bs->K*", "LCSR-pole"),
    ("Bs->phi", "LCSR-pole"),
])
def test_form_factor_implementations_exist(form_factor_key, impl_name):
    """Test that specific form factor implementations exist"""
    if form_factor_key in form_factor_loader.keys():
        form_factor = form_factor_loader[form_factor_key]
        if impl_name in form_factor.impl_names:
            impl = form_factor.get_impl(impl_name)
            assert impl is not None
            assert hasattr(impl, 'name')
            assert impl.name == impl_name
            
            # Test implementation properties
            assert hasattr(impl, 'config')
            assert isinstance(impl.config, dict)
            
            # Test that implementation has reference information
            assert hasattr(impl, 'ref')
            assert hasattr(impl, 'method')
            assert hasattr(impl, 'citation')


@pytest.mark.parametrize("form_factor_key,impl_name,expected_ff_count", [
    ("B->pi", "LCSR-2004", 3),      # f+, f0, fT
    ("B->pi", "LQCD-FLAG-2024", 3), # f+, f0, fT
    ("B->K", "LCSR-2004", 3),       # f+, f0, fT
    ("B->K", "LQCD-FLAG-2024", 3),  # f+, f0, fT
    ("D->pi", "LQCD-z 2017", 2),    # f+, f0
    ("D->K", "LQCD-z 2017", 2),     # f+, f0
    ("Lambda_b->Lambda", "LQCD-2016-nominal", 10), # f+, f0, fp, g+, g0, gp, h+, hp, ht+, htp
    ("Lambda_b->Lambda_1520", "LQCD-2021-nominal", 13), # f0, f+, fp, fpp, g0, g+, gp, gpp, h+, hp, hpp, ht+, htp, htpp
    ("B->rho", "LCSR-pole", 7),     # V, A0, A1, A2, T1, T2, T3
    ("B->K*", "LCSR-pole", 7),      # V, A0, A1, A2, T1, T2, T3
])
def test_form_factor_functions_count(form_factor_key, impl_name, expected_ff_count):
    """Test that implementations contain expected number of form factor functions"""
    if form_factor_key in form_factor_loader.keys():
        form_factor = form_factor_loader[form_factor_key]
        if impl_name in form_factor.impl_names:
            impl = form_factor.get_impl(impl_name)
            ff_names = impl.form_factor_names
            assert len(ff_names) == expected_ff_count, \
                f"{impl_name} should have {expected_ff_count} form factors"


@pytest.mark.parametrize("form_factor_key,impl_name", [
    ("B->pi", "LCSR-2004"),
    ("B->pi", "LQCD-FLAG-2024"),
    ("B->K", "LCSR-2004"),
    ("D->pi", "LQCD-z 2017"),
])
def test_form_factor_function_evaluation(form_factor_key, impl_name):
    """Test that form factor functions can be evaluated"""
    if form_factor_key in form_factor_loader.keys():
        form_factor = form_factor_loader[form_factor_key]
        if impl_name in form_factor.impl_names:
            impl = form_factor.get_impl(impl_name)
            ff_names = impl.form_factor_names
            
            # Test each form factor function
            for ff_name in ff_names:
                ff_func = impl.form_factor_function(ff_name)
                assert callable(ff_func), f"Form factor function for {ff_name} should be callable"
                
                # Test evaluation at q²=0
                result = ff_func(0.0)
                assert isinstance(result, (int, float)), \
                    f"Result of {ff_name} at q²=0 should be a number"
                assert not (result != result), f"Result of {ff_name} at q²=0 should not be NaN"


def test_form_factor_get_central_values():
    """Test that get_central_values method works correctly"""
    if "B->pi" in form_factor_loader.keys():
        form_factor = form_factor_loader["B->pi"]
        impl = form_factor.get_impl(form_factor.impl_names[0])
        
        # Test get_central_values method
        central_values = impl.get_central_values(0.0)
        assert isinstance(central_values, list), "get_central_values should return a list"
        assert len(central_values) == len(impl.form_factor_names), \
            "Should return one value per form factor"
        
        for value in central_values:
            assert isinstance(value, (int, float)), \
                "Each central value should be a number"
            assert not (value != value), "Central values should not be NaN"


def test_form_factor_add_impl():
    """Test adding a new implementation to a form factor"""
    if "B->pi" in form_factor_loader.keys():
        form_factor = form_factor_loader["B->pi"]
        original_impl_count = len(form_factor.impl_names)
        
        # Get a copy of an existing implementation to use as a new impl
        existing_impl = form_factor.get_impl(form_factor.impl_names[0])
        
        # We won't actually add a new impl because that would modify the object
        # but we can test that the method exists and has the right signature
        assert hasattr(form_factor, 'add_impl')
        assert callable(form_factor.add_impl)


def test_form_factor_error_handling():
    """Test error handling in form factor methods"""
    if "B->pi" in form_factor_loader.keys():
        form_factor = form_factor_loader["B->pi"]
        
        # Test getting non-existent implementation
        with pytest.raises(KeyError):
            form_factor.get_impl("NonExistentImpl")
            
        impl = form_factor.get_impl(form_factor.impl_names[0])
        
        # Test getting non-existent form factor function
        with pytest.raises(KeyError):
            impl.form_factor_function("NonExistentFF")


if __name__ == "__main__":
    pytest.main([__file__])