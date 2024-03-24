from typing import Any, Literal, Optional

from pydantic import BaseModel, Field
from typing_extensions import Unpack

from flect.types import FieldKwargs

__all__ = "Combobox", "ComboboxOption", "Input", "Select"


class ComboboxOption(BaseModel):
    label: str
    value: Any


def Combobox(
    editable: bool = True,
    placeholder: Optional[str] = None,
    options: Optional[list[ComboboxOption]] = None,
    *,
    class_name: Optional[str] = None,
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "fieldType": "combobox",
            "editable": editable,
            "className": class_name,
            "attrs": {
                "placeholder": placeholder,
                "options": [option.model_dump() for option in options] if options else None,
            },
        },
        **kwargs,
    )


def Input(
    editable: bool = True,
    type: Literal["text", "email"] = "text",
    placeholder: Optional[str] = None,
    *,
    class_name: Optional[str] = None,
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "fieldType": "input",
            "editable": editable,
            "className": class_name,
            "attrs": {
                "type": type,
                "placeholder": placeholder,
            },
        },
        **kwargs,
    )


def Select(
    editable: bool = True,
    placeholder: Optional[str] = None,
    *,
    class_name: Optional[str] = None,
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "fieldType": "select",
            "editable": editable,
            "className": class_name,
            "attrs": {
                "placeholder": placeholder,
            },
        },
        **kwargs,
    )
