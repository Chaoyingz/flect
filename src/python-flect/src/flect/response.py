from typing import Optional

from pydantic import BaseModel, Field

from flect.actions import AnyAction
from flect.component.components import AnyComponent
from flect.head import Head


class PageResponse(BaseModel):
    head: Optional[Head] = Field(default=None, description="The head of the response.")
    body: Optional[AnyComponent] = Field(default=None, description="The components of the response.")


class ActionResponse(BaseModel):
    action: AnyAction
