import typing as _t

import pydantic as _p


class Route(_p.BaseModel):
    model_config = _p.ConfigDict(extra="forbid")

    path: str = _p.Field(
        ...,
        description="The path of the route.",
    )
    index: _t.Optional[bool] = _p.Field(
        False,
        description="Whether the route is the index.",
    )
    children: _t.Optional[list["Route"]] = _p.Field(
        None,
        description="The children of the route.",
    )
