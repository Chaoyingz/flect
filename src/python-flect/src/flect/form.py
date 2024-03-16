from typing import Any, Callable, Literal, Optional, TypedDict, Union

from pydantic import AliasChoices, AliasPath, Field, types
from typing_extensions import Unpack


class FieldKwargs(TypedDict):
    default_factory: Optional[Callable[[], Any]]
    alias: Optional[str]
    alias_priority: Optional[int]
    validation_alias: Optional[Union[str, AliasPath, AliasChoices]]
    serialization_alias: Optional[str]
    title: Optional[str]
    description: Optional[str]
    examples: Optional[list[Any]]
    exclude: Optional[bool]
    discriminator: Optional[Union[str, types.Discriminator]]
    frozen: Optional[bool]
    validate_default: Optional[bool]
    repr: bool
    init: Optional[bool]
    init_var: Optional[bool]
    kw_only: Optional[bool]
    pattern: Optional[str]
    strict: Optional[bool]
    gt: Optional[float]
    ge: Optional[float]
    lt: Optional[float]
    le: Optional[float]
    multiple_of: Optional[float]
    allow_inf_nan: Optional[bool]
    max_digits: Optional[int]
    decimal_places: Optional[int]
    min_length: Optional[int]
    max_length: Optional[int]
    union_mode: Literal["smart", "left_to_right"]


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
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "fieldType": "select",
            "className": class_name,
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
