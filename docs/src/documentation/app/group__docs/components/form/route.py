import asyncio
import json

from fastapi.encoders import jsonable_encoder
from tui.actions import Notify
from tui.response import ActionResponse

from documentation.app.group__docs.components.dynamic__component_type.page import FormExampleModel


async def post(form: FormExampleModel) -> ActionResponse:
    await asyncio.sleep(0.1)
    return ActionResponse(
        action=Notify(
            title="You submitted the following values:",
            description=json.dumps(jsonable_encoder(form), indent=2),
        )
    )
