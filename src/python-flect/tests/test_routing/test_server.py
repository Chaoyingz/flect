from fastapi.routing import APIRoute
from flect.constants import NAVIGATION_ROUTE_PATH
from flect.routing.server import (
    generate_api_routes,
    generate_loader_routes,
    generate_navigation_routes,
    generate_server_side_render_routes,
    generate_sitemap_routes,
    get_app_router,
    sort_routes_by_path,
)


def test_generate_navigation_routes(client_routes, client):
    routes = generate_navigation_routes(client_routes)
    route = next(routes, None)
    client.app.routes.append(route)
    response = client.get(NAVIGATION_ROUTE_PATH)
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


def test_sort_routes():
    routes = [
        APIRoute("/a/", lambda: None, methods=["GET"]),
        APIRoute("/a/{id}/", lambda: None, methods=["GET"]),
        APIRoute("/a/b/", lambda: None, methods=["GET"]),
        APIRoute("/{path:path}", lambda: None, methods=["GET"]),
        APIRoute("/a/{id}/b/", lambda: None, methods=["GET"]),
    ]
    sorted_routes = sorted(routes, key=sort_routes_by_path)
    assert [route.path for route in sorted_routes] == [
        "/a/",
        "/a/b/",
        "/a/{id}/",
        "/a/{id}/b/",
        "/{path:path}",
    ]


def test_get_app_router(app_module):
    router = get_app_router(app_module)
    assert router.routes
