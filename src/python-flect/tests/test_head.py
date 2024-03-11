import pytest
from flect.head import TitleTemplate, merge_parent_title


@pytest.mark.parametrize(
    ("parent_title", "child_title", "expected"),
    [
        (None, TitleTemplate(default="title", absolute=False), TitleTemplate(default="title", absolute=False)),
        (
            TitleTemplate(default="title", absolute=False),
            TitleTemplate(default="title", absolute=False),
            TitleTemplate(default="title - title", absolute=False),
        ),
        (
            TitleTemplate(template="{title}-title", default="title", absolute=False),
            TitleTemplate(default="title", absolute=False),
            TitleTemplate(default="title-title", absolute=False),
        ),
        (
            TitleTemplate(template="{title}-title", default="title", absolute=False),
            TitleTemplate(default="title", absolute=True),
            TitleTemplate(default="title", absolute=True),
        ),
    ],
)
def test_merge_parent_title(parent_title, child_title, expected):
    title = merge_parent_title(
        parent_title,
        child_title,
    )

    assert title == expected
