from typing import Annotated

from fastapi import Path
from flect import PageResponse
from flect import components as c

from tests.app.utils import get_relative_path_text


async def page(segment_id: Annotated[int, Path(..., description="The ID of the dynamic segment")]) -> PageResponse:
    return PageResponse(body=c.Button(children=[c.Text(text=get_relative_path_text(__file__))]))
