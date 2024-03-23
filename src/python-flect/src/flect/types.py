from typing import Annotated, Any, Callable, Literal, Optional, TypedDict, Union

import pydantic
from pydantic import AliasChoices, AliasPath, types
from pydantic_core import core_schema


class JsonDataSchema:
    @staticmethod
    def __get_pydantic_json_schema__(
        _core_schema: core_schema.CoreSchema, handler: pydantic.GetJsonSchemaHandler
    ) -> Any:
        json_data_schema = core_schema.union_schema(
            [
                core_schema.str_schema(),
                core_schema.float_schema(),
                core_schema.bool_schema(),
                core_schema.none_schema(),
                core_schema.list_schema(core_schema.definition_reference_schema("JsonData")),
                core_schema.dict_schema(core_schema.str_schema(), core_schema.definition_reference_schema("JsonData")),
            ],
            ref="JsonData",
        )
        return handler(json_data_schema)


JsonData = Annotated[Any, JsonDataSchema()]


class FieldKwargs(TypedDict, total=False):
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
