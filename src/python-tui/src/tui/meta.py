from typing import Optional

from pydantic import BaseModel


class Meta(BaseModel):
    description: Optional[str] = None
