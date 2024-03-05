import uuid
from typing import Annotated

from pydantic import BaseModel, Field

from flect import PageResponse
from flect import components as c
from flect import form

from todo.storage import storage


class TodoInCreate(BaseModel):
    name: Annotated[str, form.Input(placeholder="Enter task name...")] = Field(..., max_length=16)


class TodoInDB(TodoInCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


async def page() -> PageResponse:
    todos = [TodoInDB(**todo) for todo in storage.list()]
    return PageResponse(
        element=c.Container(
            tag="section",
            children=[
                c.Form(
                    model=TodoInCreate,
                    submit_url="/",
                    class_name="mb-5 border p-5",
                ),
                c.Table(
                    datasets=todos,
                )
            ],
        ),
    )
