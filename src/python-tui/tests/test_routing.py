import pathlib

import pytest
from tui.routing import (
    build_routes_from_folder,
    configure_app_router,
    get_loader_router,
    get_pre_render_router,
    get_routes_router,
    load_module,
)

from docs.src.documentation import app


def test_load_module_success():
    module = load_module(pathlib.Path(app.__file__))
    assert module is not None


def test_load_module_failure(tmp_path):
    with pytest.raises(ImportError):
        load_module(tmp_path)


def test_build_routes_from_folder():
    routes = build_routes_from_folder(pathlib.Path(app.__file__).parent)
    assert routes


@pytest.fixture()
def routes():
    routes = build_routes_from_folder(pathlib.Path(app.__file__).parent)
    return routes


def test_get_routes_router(routes):
    router = get_routes_router(routes)
    assert router


def test_get_loader_router(routes):
    router = get_loader_router(routes)
    assert router


def test_get_pre_render_router(routes):
    router = get_pre_render_router(routes)
    assert router


def test_configure_app_router(routes):
    router = configure_app_router(app)
    assert router
