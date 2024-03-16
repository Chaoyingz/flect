from typing import Literal, Optional

from flect import components as c


class BaseUIComponent(c.Custom):
    package: Literal["docs-ui"] = "docs-ui"
    sub_type: Literal["badge"] = "badge"


class Badge(BaseUIComponent):
    package: Literal["docs-ui"] = "docs-ui"
    sub_type: Literal["badge"] = "badge"
    class_name: Optional[str] = None
    text: str
