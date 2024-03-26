from flect import ActionResponse
from flect import actions as a

from tests.app.utils import get_relative_path_text


async def post() -> ActionResponse:
    return ActionResponse(action=a.Redirect(path=get_relative_path_text(__file__)))
