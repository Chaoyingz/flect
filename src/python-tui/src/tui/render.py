from contextlib import AsyncExitStack
from typing import Optional

from fastapi import Request
from fastapi.dependencies.utils import request_params_to_args, solve_dependencies
from fastapi.routing import APIRoute
from starlette._utils import get_route_path

from tui import components as c
from tui.response import Response


def generate_html(
    meta_html: str = "",
    element_html: str = "",
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
            <script type="module" src="/static/assets/index.js"></script>
            <link rel="stylesheet" href="/static/assets/index.css" />
            {meta_html}
        </head>
        <body>
            <div class="absolute invisible h-0 w-0">{element_html}</div>
            <div id="root"></div>
        </body>
    </html>
    """


async def get_route_response(
    request: Request, route: APIRoute, outlet: Optional[c.AnyComponent] = None
) -> Optional[Response]:
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
        path_values, path_errors = request_params_to_args(route.dependant.path_params, request.path_params)
        query_values, query_errors = request_params_to_args(route.dependant.query_params, request.query_params)
        header_values, header_errors = request_params_to_args(route.dependant.header_params, request.headers)
        cookie_values, cookie_errors = request_params_to_args(route.dependant.cookie_params, request.cookies)
        values.update(path_values)
        values.update(query_values)
        values.update(header_values)
        values.update(cookie_values)
        if outlet is not None:
            values["outlet"] = outlet
        if route.dependant.call:
            return await route.dependant.call(**values)
    return None


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
    Optional[str]
    """
    loader_path = root_router_prefix + get_route_path(request.scope)

    response = None

    for route in routes:
        match = route.path_regex.match(loader_path)
        if match:
            matched_params = match.groupdict()
            for key, value in matched_params.items():
                matched_params[key] = route.param_convertors[key].convert(value)
            request.scope.get("path_params", {}).update(matched_params)
            response = await get_route_response(request, route)

    element = response.element
    meta = response.meta

    layout_path = loader_path + layout_router_suffix
    layout_routes = [r for r in routes if r.path.endswith(layout_router_suffix)]

    while layout_path.startswith(root_router_prefix):
        for layout_route in layout_routes:
            match = layout_route.path_regex.match(layout_path)
            if match:
                matched_params = match.groupdict()
                for key, value in matched_params.items():
                    matched_params[key] = layout_route.param_convertors[key].convert(value)
                request.scope.get("path_params", {}).update(matched_params)
                layout_response = await get_route_response(request, layout_route, element)
                if layout_response:
                    element = layout_response.element
                    if layout_response.meta:
                        if meta is None:
                            meta = layout_response.meta
                            continue
                        if meta.title and not meta.title.absolute:
                            meta.title.apply_parent_title(layout_response.meta.title)
                        if meta.description is None:
                            meta.description = layout_response.meta.description
                        if meta.keywords is None:
                            meta.keywords = layout_response.meta.keywords
        # Iteratively trim path segments and append layout suffix, e.g., from '/a/b_layout/' to '/a_layout/'
        layout_path = "/".join(layout_path.rsplit("/", 3)[:-3]) + "/" + layout_router_suffix

    return meta.render_to_html() if meta else "", element.render_to_html() if element else ""
