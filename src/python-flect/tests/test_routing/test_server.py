from flect.constants import NAVIGATION_ROUTE_PATH, ROOT_ROUTE_PREFIX
from flect.routing.server import (
    generate_api_routes,
    generate_loader_routes,
    generate_navigation_routes,
    generate_server_side_render_routes,
    generate_sitemap_routes,
    get_app_router,
)


def test_generate_navigation_routes(client_routes, client):
    routes = generate_navigation_routes(client_routes)
    route = next(routes, None)
    client.app.routes.append(route)
    response = client.get(f"{ROOT_ROUTE_PREFIX}{NAVIGATION_ROUTE_PATH}")
    assert response.status_code == 200
    assert response.json() == [route.model_dump() for route in client_routes]


def test_generate_loader_routes(client_routes):
    routes = generate_loader_routes(client_routes)
    assert list(routes)


def test_generate_api_routes(app_folder):
    routes = generate_api_routes(app_folder)
    routes_list = list(routes)
    assert len(routes_list) == 4


def test_generate_server_side_render_routes(client_routes, loader_routes, client):
    routes = generate_server_side_render_routes(client_routes, loader_routes)
    route = next(routes, None)
    client.app.routes.append(route)
    response = client.get("/")
    assert response.status_code == 200
    assert response.text


def test_generate_sitemap_routes(client_routes, client):
    route = generate_sitemap_routes(client_routes)
    client.app.routes.append(next(route))
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert response.text


def test_get_app_router(app_module):
    router = get_app_router(app_module)
    assert router.routes
