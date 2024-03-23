from typing import Optional

from flect import components as c
from pydantic import BaseModel
from pydantic_core import PydanticUndefined


class APIReference(BaseModel):
    prop: str
    type: str
    default: Optional[str]
    description: Optional[str]


def get_api_reference_section(component: c.AnyComponent) -> c.Container:
    props = []
    for field, filed_info in component.model_fields.items():
        if field in ["type", "type"]:
            continue
        if field == "children":
            filed_info.annotation = "flect.components.AnyComponents"
            filed_info.default = "[]"
            filed_info.description = "The children of the component."
        if filed_info.default == PydanticUndefined:
            filed_info.default = "None"
        props.append(
            APIReference(
                prop=field,
                type=str(filed_info.annotation),
                default=filed_info.default,
                description=filed_info.description,
            )
        )
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=2,
                text="API Reference",
                class_name="text-2xl mb-6 border-b pb-2",
            ),
            c.Table(model=APIReference, datasets=props),
        ],
    )
