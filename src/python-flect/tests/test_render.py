import re

import pytest
from fastapi import FastAPI, Request
from flect import PageResponse
from flect import components as c
from flect.render import generate_html, get_route_response, render_server_side_html

from tests.app.utils import convert_path_to_regex_str


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


async def test_resolve_route_response(route_request, client_routes, loader_routes):
    response = await render_server_side_html(route_request, client_routes, loader_routes)
    assert response is not None


@pytest.mark.parametrize(
    "request_path, except_response",
    [
        ("/", {"page.py", "layout.py"}),
        ("/segment1/", {"layout.py", "segment1/layout.py", "segment1/page.py"}),
        ("/segment1/segment2/", {"layout.py", "segment1/layout.py", "segment1/segment2/page.py"}),
        (
            "/segment1/segment3/",
            {
                "layout.py",
                "segment1/layout.py",
                "segment1/group__segment2/layout.py",
                "segment1/group__segment2/segment3/page.py",
            },
        ),
        ("/segment1/0/", {"layout.py", "segment1/layout.py", "segment1/dynamic__segment_id/page.py"}),
    ],
)
async def test_render_server_side_html(app_module, client_routes, loader_routes, request_path, except_response):
    request = Request(
        scope={
            "type": "http",
            "method": "GET",
            "path": request_path,
            "query_string": "",
            "headers": {},
            "path_params": {"path": request_path},
        }
    )
    _, body = await render_server_side_html(
        request,
        client_routes,
        loader_routes,
    )
    pattern = re.compile(r"(\^.*?\$)", re.MULTILINE)
    matches = pattern.findall(body)
    except_response = set((convert_path_to_regex_str(r)) for r in except_response)
    assert except_response == set(matches)
