from tui.actions import Notify
from tui.response import ActionResponse

from documentation.app.docs.components._component_type.page import FormExampleModel


async def post(form: FormExampleModel) -> ActionResponse:
    return ActionResponse(action=Notify(title=f"hello {form.username}"))
