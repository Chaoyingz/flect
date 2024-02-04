from contextlib import AsyncExitStack
from typing import Optional

from fastapi import Request
from fastapi.dependencies.utils import solve_dependencies
from fastapi.routing import APIRoute
from starlette._utils import get_route_path

from tui import components as c

STATIC_ASSETS_URL = "http://localhost:7777/dist"


def get_prebuild_html(
    title: str,
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
            <title>{title}</title>
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
) -> c.AnyComponent:
    async with AsyncExitStack() as async_exit_stack:
        values, *_ = await solve_dependencies(
            request=request,
            dependant=route.dependant,
            async_exit_stack=async_exit_stack,
        )
    if outlet is not None:
        values["outlet"] = outlet
    return await route.dependant.call(**values)


async def get_pre_render_html(
    request: Request,
    routes: list[APIRoute],
) -> Optional[str]:
    route_path = "/tui" + get_route_path(request.scope)
    routes = [r for r in routes if r.name != "prebuild"]
    for route in routes:
        if not route.path_regex.match(route_path):
            continue

        component = await get_route_response(request, route)
        layout_path = route_path + "_layout/"
        while layout_path.startswith("/tui"):
            try:
                matched_path = next(r for r in routes if r.path_regex.match(layout_path))
            except StopIteration:
                ...
            else:
                component = await get_route_response(request, matched_path, component)
            finally:
                layout_path = "/".join(layout_path.rsplit("/", 3)[:-3]) + "/_layout/"
        return component.render_to_html()

    return None
