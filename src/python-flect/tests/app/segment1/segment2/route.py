from flect import ActionResponse
from flect import actions as a


async def post() -> ActionResponse:
    return ActionResponse(action=a.Redirect(path=""))
