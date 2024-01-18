from fastapi import FastAPI

from tui.prebuild import add_prebuild_route


def init_tui(
    app: FastAPI,
    *,
    title: str = "tui",
    static_assets_url: str = "https://cdn.jsdelivr.net/npm/@chaoying/npm-tui@0.1.3/dist",
) -> None:
    add_prebuild_route(app, title, static_assets_url)
