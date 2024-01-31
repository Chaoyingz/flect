import pathlib

import pytest
from tui.route import get_routes
from tui.router import get_page_router, get_routes_router

from docs import app


@pytest.fixture()
def routes():
    folder = pathlib.Path(app.__file__).parent
    routes = get_routes(folder)
    return routes


def test_get_routes_router(routes):
    router = get_routes_router(routes)
    assert router


def test_get_page_router(routes):
    router = get_page_router(routes)
    assert router
