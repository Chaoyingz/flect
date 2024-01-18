from fastapi import FastAPI
from starlette.responses import HTMLResponse


def get_prebuild_html(title: str, static_assets_url: str) -> str:
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
                src="{static_assets_url}/assets/index.js"
            ></script>
            <link
                rel="stylesheet"
                crossorigin
                href="{static_assets_url}/assets/index.css"
            />
        </head>
        <body>
            <div id="root"></div>
        </body>
    </html>
        """
    return prebuild_html


def add_prebuild_route(
    app: FastAPI,
    title: str,
    static_assets_url: str,
) -> None:
    @app.get("/{path:path}")
    async def prebuild():
        return HTMLResponse(get_prebuild_html(title, static_assets_url))
