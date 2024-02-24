import pathlib

import pytest
from tui.routing import get_client_route_objs

from docs.src.documentation import app


@pytest.fixture()
def client_routes():
    routes = get_client_route_objs(pathlib.Path(app.__file__).parent)
    return routes
