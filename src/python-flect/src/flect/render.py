from contextlib import AsyncExitStack
from typing import Optional

from fastapi import Request
from fastapi.dependencies.utils import request_params_to_args, solve_dependencies
from fastapi.routing import APIRoute
from starlette._utils import get_route_path

from flect import components as c
from flect.constants import CLIENT_LAYOUT_ROUTER_SUFFIX, CLIENT_ROOT_ROUTER_PREFIX, GROUP_ROUTE_PREFIX
from flect.head import Head, merge_head
from flect.response import PageResponse
from flect.version import VERSION


def generate_html(
    head_html: str = "",
    element_html: str = "",
) -> str:
    """
    Generates the HTML document for the given head and element HTML.

    Parameters
    ----------
    head_html : str, optional
        The server-rendered head HTML to be embedded in the template.
    element_html : str, optional
        The server-rendered body HTML to be embedded in the template.

    Returns
    -------
    str
        The complete HTML document as a string.
    """
    return f"""\
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <link rel="icon" type="image/svg+xml" href="/vite.svg" />
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500&display=swap" rel="stylesheet" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <script type="module" src="/static/assets/index-{VERSION}.js"></script>
            <link rel="stylesheet" href="/static/assets/index-{VERSION}.css" />
            {head_html}
        </head>
        <body>
            <div class="absolute invisible h-0 w-0 overflow-hidden">{element_html}</div>
            <div id="root"></div>
        </body>
    </html>
    """


async def get_route_response(
    request: Request, route: APIRoute, outlet: Optional[c.AnyComponent] = None
) -> PageResponse:
    """
    Obtains a response from a route given a request and optional outlet component.

    Parameters
    ----------
    request : Request
        The request object.
    route : APIRoute
        The route for which the response is to be obtained.
    outlet : Optional[c.AnyComponent], optional
        An optional outlet component to be included in the response, by default None.

    Returns
    -------
    Optional[c.AnyComponent]
        The component to be rendered, if any.
    """
    async with AsyncExitStack() as async_exit_stack:
        values, *_ = await solve_dependencies(
            request=request, dependant=route.dependant, async_exit_stack=async_exit_stack
        )
        param_types = ["path_params", "query_params", "header_params", "cookie_params"]
        for param_type in param_types:
            values_update, errors_update = request_params_to_args(
                getattr(route.dependant, param_type), getattr(request, param_type, {})
            )
            values.update(values_update)
        if outlet is not None:
            values["outlet"] = outlet
        assert route.dependant.call, "Route is not callable"
        response = await route.dependant.call(**values)
        if not isinstance(response, PageResponse):
            raise ValueError("Route expected a PageResponse object")
        return response
    raise ValueError("Route is not returning a PageResponse")


async def resolve_route_response(
    request: Request,
    routes: list[APIRoute],
    path: str,
    is_layout: bool = False,
    children_head: Optional[Head] = None,
    children_body: Optional[c.AnyComponent] = None,
) -> tuple[Optional[Head], Optional[c.AnyComponent]]:
    for route in routes:
        if is_layout != route.path.endswith(CLIENT_LAYOUT_ROUTER_SUFFIX):
            continue
        match = route.path_regex.match(path)
        if match:
            matched_params = {
                key: route.param_convertors[key].convert(value) for key, value in match.groupdict().items()
            }
            request.scope.get("path_params", {}).update(matched_params)
            # response will merge the children element
            response = await get_route_response(request, route, children_body)
            head = merge_head(response.head or Head(), children_head or Head())
            return head, response.body
    return None, None


async def handle_route_response(
    route: APIRoute,
    path: str,
    request: Request,
    children_head: Optional[Head] = None,
    children_body: Optional[c.AnyComponent] = None,
) -> PageResponse:
    match = route.path_regex.match(path)
    if match:
        matched_params = {key: route.param_convertors[key].convert(value) for key, value in match.groupdict().items()}
        request.scope.get("path_params", {}).update(matched_params)
        # response will merge the children element
        response = await get_route_response(request, route, children_body)
        response.head = merge_head(response.head or Head(), children_head or Head())
        return response
    raise ValueError("Route is not returning a PageResponse")


def get_matched_layout_route(
    path: str,
    routes: list[APIRoute],
):
    group_layout_paths = {r.path.split(GROUP_ROUTE_PREFIX, 1)[0]: r for r in routes if GROUP_ROUTE_PREFIX in r.path}
    while path.startswith(CLIENT_ROOT_ROUTER_PREFIX):
        layout_path = path + CLIENT_LAYOUT_ROUTER_SUFFIX
        matched_route = next((r for r in routes if r.path_regex.match(layout_path)), None)
        if matched_route:
            yield matched_route, layout_path
        if path in group_layout_paths:
            group_route = group_layout_paths[path]
            group_name = group_route.path.strip("/").split("/")[-1]
            group_path = path + group_name + "/"
            yield group_route, group_path
        path = "/".join(path.rsplit("/", 2)[:-2]) + "/"


async def render_server_side_html(
    request: Request,
    routes: list[APIRoute],
) -> tuple[str, str]:
    """
    Renders the server-side HTML for a request by resolving the appropriate
    component based on the request's path, including handling layouts.

    Parameters
    ----------
    request : Request
        The request object.
    routes : list[APIRoute]
        The list of routes to match against the request.

    Returns
    -------
    tuple[str, str]
        the head HTML strings
        the server-rendered body HTML string
    """
    request_path = CLIENT_ROOT_ROUTER_PREFIX + get_route_path(request.scope)
    matched_page_route = next((r for r in routes if r.path_regex.match(request_path)), None)
    if not matched_page_route:
        return "", ""
    page_response = await handle_route_response(
        matched_page_route,
        request_path,
        request,
    )
    for layout_route, layout_path in get_matched_layout_route(request_path, routes):
        layout_response = await handle_route_response(
            layout_route,
            layout_path,
            request,
            children_head=page_response.head,
            children_body=page_response.body,
        )
        page_response.head = layout_response.head or page_response.head
        page_response.body = layout_response.body or page_response.body
    return (
        page_response.head.render_to_html() if page_response.head else "",
        page_response.body.render_to_html() if page_response.body else "",
    )
