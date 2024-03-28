import pathlib

import pytest
from fastapi import FastAPI
from flect.routing.client import get_client_routes
from flect.routing.server import generate_loader_routes
from flect.routing.sort import path_priority
from starlette.testclient import TestClient

# from flect.routing import get_client_loader_router, get_client_routes
from tests import app as test_app_module

APP_FOLDER = pathlib.Path(test_app_module.__file__).parent


@pytest.fixture(scope="session")
def app_module():
    return test_app_module


@pytest.fixture(scope="session")
def app_folder():
    return APP_FOLDER


@pytest.fixture(scope="session")
def client_routes(app_folder):
    routes = get_client_routes(app_folder)
    return routes


@pytest.fixture(scope="session")
def loader_routes(client_routes):
    loader_routes = generate_loader_routes(client_routes)
    return sorted(loader_routes, key=lambda r: path_priority(r.path))


@pytest.fixture
def app():
    return FastAPI()


@pytest.fixture
def client(app):
    return TestClient(app)
