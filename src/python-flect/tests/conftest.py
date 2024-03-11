import pathlib

import pytest
from flect.routing import get_client_loader_router, get_client_routes

from tests import app

APP_FOLDER = pathlib.Path(app.__file__).parent


@pytest.fixture(scope="session")
def app_module():
    return app


@pytest.fixture(scope="session")
def app_folder():
    return APP_FOLDER


@pytest.fixture(scope="session")
def client_routes(app_folder):
    routes = get_client_routes(app_folder)
    return routes


@pytest.fixture(scope="session")
def loader_routes(client_routes):
    loader_router = get_client_loader_router(client_routes)
    return loader_router.routes
