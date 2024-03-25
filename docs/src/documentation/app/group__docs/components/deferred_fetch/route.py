import asyncio

from flect import components as c
from flect.response import PageResponse


async def get() -> PageResponse:
    await asyncio.sleep(0.1)
    return PageResponse(
        body=c.Container(
            tag="div",
            children=[
                c.Heading(
                    level=1,
                    text="Hello deferred fetch!",
                ),
            ],
        )
    )
