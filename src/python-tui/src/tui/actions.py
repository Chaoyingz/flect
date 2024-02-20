from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field


class Notify(BaseModel):
    action_type: Literal["notify"] = "notify"

    title: str = Field(..., description="The title of the notification.")
    description: Optional[str] = Field(None, description="The description of the notification.")
    position: Optional[
        Literal["top-left", "top-right", "bottom-left", "bottom-right", "top-center", "bottom-center"]
    ] = Field(None, description="Position of the toast.")
    type: Optional[Literal["normal", "action", "success", "info", "warning", "error", "loading", "default"]] = Field(
        None, description="Type of the toast."
    )


AnyAction = Annotated[
    Notify,
    Field(discriminator="action_type"),
]
