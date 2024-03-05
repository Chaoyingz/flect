from flect.actions import Notify
from flect.response import ActionResponse

from todo.app.page import TodoInCreate, TodoInDB
from todo.storage import storage


async def post(form: TodoInCreate) -> ActionResponse:
    storage.insert(TodoInDB(**form.dict()).model_dump())
    return ActionResponse(
        action=Notify(title="success", type="success", description=f"todo {form.name} created."),
    )
