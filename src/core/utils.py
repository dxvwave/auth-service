from functools import wraps

from db.db_helper import db_session_manager


def provide_session(func):
    @wraps(func)
    async def wrapper(self, request, context):
        async with db_session_manager.sessionmaker() as session:
            return await func(self, request, context, session=session)
    return wrapper
