import tui.components as c
from fastapi import Path


async def page(
    ctype: str = Path(..., description="The component type to render"),
) -> c.AnyComponent:
    print("ctype:", ctype)
    return c.Text(
        text=ctype,
    )
