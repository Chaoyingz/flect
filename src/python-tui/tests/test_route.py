import pathlib

from tui.route import get_routes

from docs import app


def test_get_routes():
    folder = pathlib.Path(app.__file__).parent
    routes = get_routes(folder)
    print(routes)
    assert routes
