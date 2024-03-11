import pytest
from flect.routing import (
    configure_app_router,
    get_client_loader_router,
    get_client_routes,
    get_client_routes_router,
    get_server_api_router,
    get_server_pre_render_router,
    get_server_sitemap_router,
    load_module,
)


def test_load_module_success(app_folder):
    module = load_module(app_folder / "page.py")
    assert module is not None


def test_load_module_failure(tmp_path):
    with pytest.raises(ImportError):
        load_module(tmp_path)


def test_get_client_routes(app_folder):
    routes = get_client_routes(app_folder)
    assert routes


def test_get_client_routes_router(client_routes):
    router = get_client_routes_router(client_routes)
    assert router.routes


def test_get_client_loader_router(client_routes):
    router = get_client_loader_router(client_routes)
    assert router.routes


def test_get_server_api_router(app_folder):
    router = get_server_api_router(app_folder)
    assert router.routes


def test_get_server_pre_render_router(client_routes, loader_routes):
    router = get_server_pre_render_router(client_routes, loader_routes)
    assert router.routes


def test_get_server_sitemap_router(client_routes):
    router = get_server_sitemap_router(client_routes)
    assert router


def test_configure_app_router(app_module):
    router = configure_app_router(app_module)
    assert router
