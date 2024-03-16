from contextlib import AsyncExitStack
from typing import TYPE_CHECKING, Optional

from fastapi import Request
from fastapi.dependencies.utils import solve_dependencies
from fastapi.routing import APIRoute
from starlette._utils import get_route_path
from starlette.routing import compile_path

from flect import components as c
from flect.constants import CLIENT_LAYOUT_ROUTER_SUFFIX, CLIENT_ROOT_ROUTER_PREFIX
from flect.head import Head, merge_head
from flect.response import PageResponse

if TYPE_CHECKING:
    from flect.routing import ClientRoute

# FLECT_PREBUILT_VERSION = "0.2.0"
# FLECT_PREBUILT_URI = f"https://cdn.jsdelivr.net/npm/@chaoying/flect-prebuilt@{FLECT_PREBUILT_VERSION}/dist/assets"
FLECT_PREBUILT_URI = "https://unpkg.com/@chaoying/flect-prebuilt@0.2.2-beta.0/dist/assets"


def generate_html(
    head_html: str = "",
    element_html: str = "",
    prebuilt_uri: Optional[str] = None,
) -> str:
    """
    Generates the HTML document for the given head and element HTML.

    Parameters
    ----------
    prebuilt_uri : str, optional
        The prebuilt URI to be used in the template.
    head_html : str, optional
        The server-rendered head HTML to be embedded in the template.
    element_html : str, optional
        The server-rendered body HTML to be embedded in the template.

    Returns
    -------
    str
        The complete HTML document as a string.
    """
    if prebuilt_uri is None:
        prebuilt_uri = FLECT_PREBUILT_URI
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
            <script type="module" src="{prebuilt_uri}/index.js"></script>
            <link rel="stylesheet" href="{prebuilt_uri}/index.css" />
            {head_html}
        </head>
        <body>
            <div class="sr-only">{element_html}</div>
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
        if outlet is not None:
            values["outlet"] = outlet
        assert route.dependant.call, "Route is not callable"
        response = await route.dependant.call(**values)
        if not isinstance(response, PageResponse):
            raise ValueError("Route expected a PageResponse object")
        return response
    raise ValueError("Route is not returning a PageResponse")


async def handle_route_response(
    route: APIRoute,
    path: str,
    request: Request,
    children_head: Optional[Head] = None,
    children_body: Optional[c.AnyComponent] = None,
) -> PageResponse:
    match = route.path_regex.match(path)
    if not match:
        raise ValueError("Route is not returning a PageResponse")
    matched_params = {key: route.param_convertors[key].convert(value) for key, value in match.groupdict().items()}
    request.scope.setdefault("path_params", {}).update(matched_params)
    # response will merge the children element
    response = await get_route_response(request, route, children_body)
    response.head = merge_head(response.head or Head(), children_head or Head())
    return response


def get_matched_client_route(
    path: str,
    client_routes: list["ClientRoute"],
) -> Optional["ClientRoute"]:
    for route in client_routes:
        path_regex, *_ = compile_path(route.path)
        if path_regex.match(path):
            return route
        if route.children:
            matched_route = get_matched_client_route(path, route.children)
            if matched_route:
                return matched_route
    return None


def get_matched_route(routes, path):
    return next((r for r in routes if r.path_regex.match(path)), None)


async def render_server_side_html(
    request: Request,
    client_routes: list["ClientRoute"],
    loader_routes: list[APIRoute],
) -> tuple[str, str]:
    """
    Renders the server-side HTML for a request by resolving the appropriate
    component based on the request's path, including handling layouts.

    Parameters
    ----------
    request : Request
        The request object.
    client_routes : list[APIRoute]
        The list of client-side routes to match against the request.
    loader_routes : list[APIRoute]
        The list of routes to match against the request.

    Returns
    -------
    tuple[str, str]
        the head HTML strings
        the server-rendered body HTML string
    """
    request_path = get_route_path(request.scope)
    loader_path = CLIENT_ROOT_ROUTER_PREFIX + request_path
    matched_page_route = get_matched_route(loader_routes, loader_path)
    if not matched_page_route:
        return "", ""

    page_response = await handle_route_response(
        matched_page_route,
        loader_path,
        request,
    )

    matched_client_route = get_matched_client_route(request_path, client_routes)
    if matched_client_route:
        absolute_path = matched_client_route.absolute_path
        if matched_client_route.index:
            layout_path = (
                CLIENT_ROOT_ROUTER_PREFIX
                + "/".join(absolute_path.rsplit("/", 3)[:-3])
                + "/"
                + CLIENT_LAYOUT_ROUTER_SUFFIX
            )
        else:
            layout_path = CLIENT_ROOT_ROUTER_PREFIX + absolute_path + CLIENT_LAYOUT_ROUTER_SUFFIX
        while layout_path.startswith(CLIENT_ROOT_ROUTER_PREFIX):
            matched_layout_route = get_matched_route(loader_routes, layout_path)
            if matched_layout_route:
                layout_response = await handle_route_response(
                    matched_layout_route,
                    layout_path,
                    request,
                    children_head=page_response.head,
                    children_body=page_response.body,
                )
                page_response.head = layout_response.head or page_response.head
                page_response.body = layout_response.body or page_response.body
            layout_path = "/".join(layout_path.rsplit("/", 3)[:-3]) + "/" + CLIENT_LAYOUT_ROUTER_SUFFIX

    head_html = page_response.head.render_to_html() if page_response.head else ""
    element_html = page_response.body.render_to_html() if page_response.body else ""
    return head_html, element_html
