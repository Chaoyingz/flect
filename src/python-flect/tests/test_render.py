import re

import pytest
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute, APIRouter
from flect import PageResponse
from flect import components as c
from flect.constants import DYNAMIC_ROUTE_PREFIX, GROUP_ROUTE_PREFIX
from flect.render import generate_html, get_route_response, render_server_side_html
from flect.routing import CLIENT_LAYOUT_ROUTER_SUFFIX, CLIENT_ROOT_ROUTER_PREFIX


def test_generate_html():
    test_html = "Test HTML"
    result = generate_html(test_html)
    assert test_html in result
    assert "<!DOCTYPE html>" in result


@pytest.fixture()
async def endpoint():
    async def route_endpoint() -> PageResponse:
        return PageResponse(body=c.Button(children=[c.Text(text="Hello flect!")]))

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


async def test_resolve_route_response(app, route_request):
    response = await render_server_side_html(
        route_request, app.routes
    )
    assert response is not None


@pytest.mark.parametrize(
    "request_path, response_tags",
    [
        ("/", {"tag-layout-l1", "tag-page-l1"}),
        ("/l2/", {"tag-layout-l1", "tag-group-l2", "tag-layout-l2", "tag-page-l2"}),
        ("/l2/l3/", {"tag-layout-l1", "tag-group-l2", "tag-layout-l2", "tag-page-l3"}),
    ],
)
async def test_render_server_side_html(
    request_path, response_tags
):
    router = APIRouter(prefix=CLIENT_ROOT_ROUTER_PREFIX)

    @router.get(f"/{CLIENT_LAYOUT_ROUTER_SUFFIX}")
    async def layout_endpoint(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
        return PageResponse(body=c.Container(children=[c.Text(text="tag-layout-l1"), outlet]))

    @router.get("/")
    async def page_endpoint() -> PageResponse:
        return PageResponse(body=c.Button(children=[c.Text(text="tag-page-l1")]))

    @router.get(f"/l2/{GROUP_ROUTE_PREFIX}l2/")
    async def l2_group_endpoint(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
        return PageResponse(body=c.Container(children=[c.Text(text="tag-group-l2"), outlet]))

    @router.get(f"/l2/{CLIENT_LAYOUT_ROUTER_SUFFIX}")
    async def l2_layout_endpoint(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
        return PageResponse(body=c.Container(children=[c.Text(text="tag-layout-l2"), outlet]))

    @router.get(f"/l2/")
    async def l2_page_endpoint() -> PageResponse:
        return PageResponse(body=c.Text(text="tag-page-l2"))

    @router.get(f"/l2/l3/")
    async def l3_page_endpoint() -> PageResponse:
        return PageResponse(body=c.Text(text="tag-page-l3"))

    request = Request(scope={"type": "http", "method": "GET", "path": request_path, "query_string": "", "headers": {}})
    _, body = await render_server_side_html(
        request, router.routes,
    )
    tags = re.findall(r'tag-(?:page|layout|group)-l\d+', body)
    assert set(tags) == response_tags
