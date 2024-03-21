from typing import Any

from pydantic import Field
from typing_extensions import Unpack

from flect.types import FieldKwargs


def TextDisplay(
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "displayType": "text",
        },
        **kwargs,
    )


def BooleanDisplay(
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "displayType": "boolean",
        },
        **kwargs,
    )
