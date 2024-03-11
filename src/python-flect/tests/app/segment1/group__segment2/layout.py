from flect import PageResponse
from flect import components as c

from tests.app.utils import get_relative_path_text


async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(body=c.Container(children=[c.Text(text=get_relative_path_text(__file__)), outlet]))
