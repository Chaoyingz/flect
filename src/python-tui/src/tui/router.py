import pathlib
from types import ModuleType

from fastapi import APIRouter

from tui import components as c
from tui.route import Route, RouteComponent, get_routes


def get_route_components(routes: list[Route]) -> RouteComponent:
    route_components = []
    for route in routes:
        route_component = RouteComponent(**route.model_dump(exclude={"endpoint", "layout", "children"}), children=[])
        if route.children:
            route_component.children.append(get_route_components(route.children))
        route_components.append(route_component)
    return route_components


def get_routes_router(routes: list[Route]) -> APIRouter:
    router = APIRouter()

    @router.get("/_route", response_model=RouteComponent)
    async def get_root_routes() -> RouteComponent:
        return get_route_components(routes)

    return router


def get_page_router(routes: list[Route], router: APIRouter = APIRouter()) -> APIRouter:
    for route in routes:
        router.add_api_route(
            route.pathname,
            route.endpoint,
            response_model=c.AnyComponents,
        )
        if route.children:
            get_page_router(route.children, router)
    return router


def get_layout_router(
    routes: list[Route],
    router: APIRouter = APIRouter(),
) -> APIRouter:
    for route in routes:
        router.add_api_route(
            route.pathname + "_layout",
            route.layout,
            response_model=c.AnyComponents,
        )
        if route.children:
            get_layout_router(route.children, router)
    return router


def get_router(app: ModuleType) -> APIRouter:
    app_folder = pathlib.Path(app.__file__).parent
    root_router = APIRouter(prefix="/tui")

    routes = get_routes(app_folder)
    root_router.include_router(get_routes_router(routes))
    root_router.include_router(get_page_router(routes))
    root_router.include_router(get_layout_router(routes))
    return root_router
