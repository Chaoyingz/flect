from typing import Annotated

from flect import PageResponse
from flect import components as c


async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        element=c.Container(
            tag="div",
            children=[
                c.Container(
                    tag="header",
                    class_name="h-14 border-b text-sm flex items-center px-6",
                    children=[
                        c.Link(
                            href="/",
                            children=[
                                c.Text(
                                    text="Todo",
                                    class_name="font-medium text-xl",
                                )
                            ],
                        ),
                    ]
                ),
                c.Container(
                    tag="main",
                    class_name="p-12",
                    children=[outlet]
                ),
                c.Container(
                    tag="footer",
                    class_name="h-14 border-t text-sm flex items-center px-6",
                    children=[
                        c.Text(
                            text="Made with ❤️ by flect",
                        )
                    ],
                )
            ],
        )
    )
