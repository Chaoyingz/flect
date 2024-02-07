import pytest
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from tui import components as c
from tui.render import generate_html, get_response_for_matched_route, get_route_response, render_server_side_html
from tui.routing import LAYOUT_ROUTER_SUFFIX, ROOT_ROUTER_PREFIX


def test_generate_html():
    test_html = "Test HTML"
    result = generate_html(test_html)
    assert test_html in result
    assert "<!DOCTYPE html>" in result


@pytest.fixture()
async def endpoint():
    async def route_endpoint() -> c.AnyComponent:
        return c.Button(children="Hello tui!")

    return route_endpoint


@pytest.fixture()
def app(endpoint):
    app = FastAPI()
    app.add_api_route("/test", endpoint, methods=["GET"])
    return app


@pytest.fixture()
def route_request():
    return Request(scope={"type": "http", "method": "GET", "path": "/test", "query_string": "", "headers": {}})


async def test_get_route_response(app, route_request):
    response = await get_route_response(route_request, app.routes[-1])
    assert response is not None


async def test_get_matched_route_component(app, route_request):
    component = await get_response_for_matched_route(route_request, "/test", app.routes)
    assert component is not None


async def test_render_server_side_html(endpoint, route_request):
    routes = [APIRoute("/tui/test", endpoint, methods=["GET"])]
    response = await render_server_side_html(route_request, routes, ROOT_ROUTER_PREFIX, LAYOUT_ROUTER_SUFFIX)
    assert response is not None
