from contextlib import asynccontextmanager
from unittest.mock import MagicMock


def make_coroutine(mock):
    async def coroutine(*args, **kwargs):
        return mock

    return coroutine


def make_context_manager(mock):
    @asynccontextmanager
    async def session_get(*args, **kwargs):
        yield mock

    return session_get


def make_session(result):
    response = MagicMock()
    response.text = make_coroutine(result)
    session = MagicMock()
    session.get = make_context_manager(response)
    return session
