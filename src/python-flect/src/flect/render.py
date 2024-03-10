from contextlib import AsyncExitStack
from typing import Optional

from fastapi import Request
from fastapi.dependencies.utils import request_params_to_args, solve_dependencies
from fastapi.routing import APIRoute
from starlette._utils import get_route_path

from flect import components as c
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
    layout_router_suffix: str,
    is_layout: bool = False,
    children_head: Optional[Head] = None,
    children_element: Optional[c.AnyComponent] = None,
) -> tuple[Optional[Head], Optional[c.AnyComponent]]:
    for route in routes:
        if is_layout != route.path.endswith(layout_router_suffix):
            continue
        match = route.path_regex.match(path)
        if match:
            matched_params = {
                key: route.param_convertors[key].convert(value) for key, value in match.groupdict().items()
            }
            request.scope.get("path_params", {}).update(matched_params)
            # response will merge the children element
            response = await get_route_response(request, route, children_element)
            head = merge_head(response.head or Head(), children_head or Head())
            return head, response.element
    return None, None


async def render_server_side_html(
    request: Request,
    routes: list[APIRoute],
    root_router_prefix: str,
    layout_router_suffix: str,
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
    root_router_prefix : str
        The root prefix of the router to prepend to paths for matching.
    layout_router_suffix : str
        The suffix to use for finding layout components.

    Returns
    -------
    tuple[str, str]
        the head HTML strings
        the server-rendered body HTML string
    """
    path = root_router_prefix + get_route_path(request.scope)
    head, element = await resolve_route_response(request, routes, path, layout_router_suffix)
    path += layout_router_suffix
    while path.startswith(root_router_prefix):
        layout_head, layout_element = await resolve_route_response(
            request, routes, path, layout_router_suffix, is_layout=True, children_head=head, children_element=element
        )
        element = layout_element or element
        head = layout_head or head
        path = "/".join(path.rsplit("/", 3)[:-3]) + "/" + layout_router_suffix
    return head.render_to_html() if head else "", element.render_to_html() if element else ""
