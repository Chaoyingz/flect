from contextlib import AsyncExitStack
from typing import Optional

from fastapi import Request
from fastapi.dependencies.utils import solve_dependencies
from fastapi.routing import APIRoute
from starlette._utils import get_route_path

from tui import components as c

STATIC_ASSETS_URL = "http://localhost:7777/dist"


def generate_html(
    server_side_html: str = "",
) -> str:
    """
    Generates an HTML template with server-rendered HTML embedded within it.

    Parameters
    ----------
    server_side_html : str, optional
        The server-rendered HTML to be embedded in the template, by default an empty string.

    Returns
    -------
    str
        The complete HTML document as a string.
    """
    prebuild_html = f"""\
        <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <link rel="icon" type="image/svg+xml" href="/vite.svg" />
            <link rel="preconnect" href="https://fonts.googleapis.com" />
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
            <link
                href="https://fonts.googleapis.com/css2?family=Outfit:wght@500&display=swap"
                rel="stylesheet"
            />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>tui</title>
            <script
                type="module"
                crossorigin
                src="{STATIC_ASSETS_URL}/assets/index.js"
            ></script>
            <link
                rel="stylesheet"
                crossorigin
                href="{STATIC_ASSETS_URL}/assets/index.css"
            />
        </head>
        <body>
            <div class="invisible h-0 w-0">{server_side_html}</div>
            <div id="root"></div>
        </body>
    </html>
        """
    return prebuild_html


async def get_route_response(
    request: Request, route: APIRoute, outlet: Optional[c.AnyComponent] = None
) -> Optional[c.AnyComponent]:
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
            request=request,
            dependant=route.dependant,
            async_exit_stack=async_exit_stack,
        )
        if outlet is not None:
            values["outlet"] = outlet
        if route.dependant.call:
            return await route.dependant.call(**values)
    return None


async def get_matched_route_component(
    request: Request, path: str, routes: list[APIRoute], outlet: Optional[c.AnyComponent] = None
) -> Optional[c.AnyComponent]:
    """
    Finds a route that matches the given path and obtains the corresponding component.

    Parameters
    ----------
    request : Request
        The request object.
    path : str
        The path to match against the available routes.
    routes : list[APIRoute]
        The list of available routes.
    outlet : Optional[c.AnyComponent], optional
        An optional component to pass as an outlet, by default None.

    Returns
    -------
    Optional[c.AnyComponent]
        The matched component, if a matching route is found; otherwise, None.
    """
    matched_route = next((route for route in routes if route.path_regex.match(path)), None)
    if matched_route:
        return await get_route_response(request, matched_route, outlet)
    return None


async def render_server_side_html(
    request: Request,
    routes: list[APIRoute],
    root_router_prefix: str,
    layout_router_suffix: str,
) -> Optional[str]:
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
    Optional[str]
        The rendered HTML string if a component is successfully resolved; otherwise, None.
    """
    request_path = root_router_prefix + get_route_path(request.scope)
    component = await get_matched_route_component(request, request_path, routes)

    layout_path = request_path + layout_router_suffix
    while layout_path.startswith(root_router_prefix):
        component_with_layout = await get_matched_route_component(request, layout_path, routes, component)
        if component_with_layout:
            component = component_with_layout
        layout_path = "/".join(layout_path.rsplit("/", 3)[:-3]) + "/" + layout_router_suffix

    return component.render_to_html() if component else None
