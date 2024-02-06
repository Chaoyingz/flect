from contextlib import AsyncExitStack
from typing import Optional

from fastapi import Request
from fastapi.dependencies.utils import solve_dependencies
from fastapi.routing import APIRoute
from starlette._utils import get_route_path

from tui import components as c

STATIC_ASSETS_URL = "http://localhost:7777/dist"


def render_html(
    server_html: str = "",
) -> str:
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
            <div class="invisible h-0 w-0">{server_html}</div>
            <div id="root"></div>
        </body>
    </html>
        """
    return prebuild_html


async def get_route_response(
    request: Request, route: APIRoute, outlet: Optional[c.AnyComponent] = None
) -> Optional[c.AnyComponent]:
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


def find_matched_route(
    path: str,
    routes: list[APIRoute],
) -> Optional[APIRoute]:
    for route in routes:
        if route.path_regex.match(path):
            return route
    return None


async def get_component(
    request: Request, route_path: str, routes: list[APIRoute], outlet: Optional[c.AnyComponent] = None
) -> Optional[c.AnyComponent]:
    matched_route = find_matched_route(route_path, routes)
    if matched_route:
        return await get_route_response(request, matched_route, outlet)
    return None


async def render_server_html(
    request: Request,
    routes: list[APIRoute],
    root_router_prefix: str,
    layout_router_suffix: str,
) -> Optional[str]:
    route_path = root_router_prefix + get_route_path(request.scope)
    component = await get_component(request, route_path, routes)

    layout_path = route_path + layout_router_suffix
    while layout_path.startswith(root_router_prefix):
        component = await get_component(request, layout_path, routes, component)
        layout_path = "/".join(layout_path.rsplit("/", 3)[:-3]) + "/" + layout_router_suffix

    return component.render_to_html() if component else None
