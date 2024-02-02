import pathlib

import pytest
from tui.routing import get_loader_router, get_router, get_routes, get_routes_router

from docs import app


def test_get_routes():
    folder = pathlib.Path(app.__file__).parent
    routes = get_routes(folder)
    assert routes


@pytest.fixture()
def routes():
    folder = pathlib.Path(app.__file__).parent
    return get_routes(folder)


def test_get_routes_router(routes):
    router = get_routes_router(routes)
    assert router


def test_get_loader_router(routes):
    router = get_loader_router(routes)
    assert router


def test_get_router():
    router = get_router(app)
    assert router
