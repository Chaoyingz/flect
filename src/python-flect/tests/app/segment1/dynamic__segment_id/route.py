from flect import ActionResponse, actions

from tests.app.utils import get_relative_path_text


async def post() -> ActionResponse:
    return ActionResponse(action=actions.Redirect(path=get_relative_path_text(__file__)))
