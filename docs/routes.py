from docs.layouts.root_layout import root_layout
from docs.pages.landing import landing_page
from tui import LayoutRouter


root_layout_router = LayoutRouter(
    layout=root_layout,
    prefix="/api",
)
root_layout_router.get(path="/")(landing_page)
