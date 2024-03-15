from typing import Annotated, Literal, Optional, Union

from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseAction(BaseModel):
    package: Literal["flect"] = "flect"
    model_config = ConfigDict(extra="forbid", alias_generator=AliasGenerator(serialization_alias=to_camel))


class Notify(BaseAction):
    type: Literal["notify"] = "notify"

    title: str = Field(..., description="The title of the notification.")
    description: Optional[str] = Field(default=None, description="The description of the notification.")
    position: Optional[
        Literal["top-left", "top-right", "bottom-left", "bottom-right", "top-center", "bottom-center"]
    ] = Field(default=None, description="Position of the toast.")
    style: Optional[Literal["normal", "action", "success", "info", "warning", "error", "loading", "default"]] = Field(
        default=None, description="Type of the toast."
    )


class Redirect(BaseAction):
    type: Literal["redirect"] = "redirect"
    url: str = Field(..., description="The URL to redirect to.")


AnyAction = Annotated[
    Union[Notify, Redirect],
    Field(discriminator="type"),
]
