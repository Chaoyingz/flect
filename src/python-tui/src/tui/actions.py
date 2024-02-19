from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field


class Notify(BaseModel):
    atype: Literal["notify"] = "notify"

    title: str = Field(..., description="The title of the notification.")
    description: Optional[str] = Field(None, description="The description of the notification.")


AnyAction = Annotated[
    Notify,
    Field(discriminator="atype"),
]
