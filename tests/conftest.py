"""Fixture for the Eiswarnung tests."""

from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession

from eiswarnung import Eiswarnung


@pytest.fixture(name="eiswarnung_client")
async def client() -> AsyncGenerator[Eiswarnung, None]:
    """Fixture for the Eiswarnung client."""
    async with (
        ClientSession() as session,
        Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        ) as eiswarnung_client,
    ):
        yield eiswarnung_client
