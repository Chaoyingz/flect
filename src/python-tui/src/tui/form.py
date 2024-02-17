from typing import Any, Literal, Optional

from pydantic import Field


def Checkbox(
    *,
    class_name: Optional[str] = None,
) -> Any:
    return Field(
        json_schema_extra={
            "ctype": "checkbox",
            "class_name": class_name,
        }
    )


def Input(
    type: Literal["text", "password", "email"] = "text",
    placeholder: Optional[str] = None,
    *,
    class_name: Optional[str] = None,
) -> Any:
    return Field(
        json_schema_extra={
            "ctype": "input",
            "class_name": class_name,
            "attrs": {
                "type": type,
                "placeholder": placeholder,
            },
        }
    )


def Select(
    *,
    class_name: Optional[str] = None,
) -> Any:
    return Field(
        json_schema_extra={
            "ctype": "select",
            "class_name": class_name,
        }
    )


def Textarea(
    rows: Optional[int] = None,
    cols: Optional[int] = None,
    placeholder: Optional[str] = None,
    *,
    class_name: Optional[str] = None,
) -> Any:
    return Field(
        json_schema_extra={
            "ctype": "textarea",
            "class_name": class_name,
            "attrs": {
                "rows": rows,
                "cols": cols,
                "placeholder": placeholder,
            },
        }
    )
