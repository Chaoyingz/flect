from typing import Any, Callable, Literal, Optional, TypedDict

from pydantic import AliasChoices, AliasPath, Field, types
from typing_extensions import Unpack


class FieldKwargs(TypedDict):
    default_factory: Callable[[], Any] | None
    alias: str | None
    alias_priority: int | None
    validation_alias: str | AliasPath | AliasChoices | None
    serialization_alias: str | None
    title: str | None
    description: str | None
    examples: list[Any] | None
    exclude: bool | None
    discriminator: str | types.Discriminator | None
    frozen: bool | None
    validate_default: bool | None
    repr: bool
    init: bool | None
    init_var: bool | None
    kw_only: bool | None
    pattern: str | None
    strict: bool | None
    gt: float | None
    ge: float | None
    lt: float | None
    le: float | None
    multiple_of: float | None
    allow_inf_nan: bool | None
    max_digits: int | None
    decimal_places: int | None
    min_length: int | None
    max_length: int | None
    union_mode: Literal["smart", "left_to_right"]


def Checkbox(
    *,
    class_name: Optional[str] = None,
    **kwargs: Unpack[FieldKwargs],
) -> Any:
    return Field(
        json_schema_extra={
            "componentType": "checkbox",
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
            "componentType": "input",
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
            "componentType": "select",
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
            "componentType": "textarea",
            "className": class_name,
            "attrs": {
                "rows": rows,
                "cols": cols,
                "placeholder": placeholder,
            },
        },
        **kwargs,
    )
