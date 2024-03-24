from typing import Any, Literal, Optional

from pydantic import Field
from typing_extensions import Unpack

from flect.types import FieldKwargs

__all__ = "Checkbox", "Input", "Select", "Textarea"


def Checkbox(
    *,
    class_name: Optional[str] = None,
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "fieldType": "checkbox",
            "className": class_name,
        },
        **kwargs,
    )


def Input(
    type: Literal["text", "password", "email"] = "text",
    placeholder: Optional[str] = None,
    *,
    class_name: Optional[str] = None,
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "fieldType": "input",
            "className": class_name,
            "attrs": {
                "type": type,
                "placeholder": placeholder,
            },
        },
        **kwargs,
    )


def Select(
    *,
    class_name: Optional[str] = None,
    placeholder: Optional[str] = None,
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "fieldType": "select",
            "className": class_name,
            "attrs": {
                "placeholder": placeholder,
            },
        },
        **kwargs,
    )


def Textarea(
    rows: Optional[int] = None,
    cols: Optional[int] = None,
    placeholder: Optional[str] = None,
    *,
    class_name: Optional[str] = None,
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "fieldType": "textarea",
            "className": class_name,
            "attrs": {
                "rows": rows,
                "cols": cols,
                "placeholder": placeholder,
            },
        },
        **kwargs,
    )
