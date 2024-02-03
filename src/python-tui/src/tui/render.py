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


def render_components_to_html(components: c.AnyComponents) -> str:
    return "".join(component.render_to_html() for component in components)
