import pytest
from flect.utils import load_module


def test_load_module_success(app_folder):
    module = load_module(app_folder / "page.py")
    assert module is not None
    assert hasattr(module, "page")


def test_load_module_failure(tmp_path):
    with pytest.raises(ImportError):
        load_module(tmp_path)
