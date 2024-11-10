"""Basic tests for the Eiswarnung API."""

# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import pytest
from aiohttp import ClientError, ClientResponse, ClientSession
from aresponses import Response, ResponsesMockServer

from eiswarnung import (
    Eiswarnung,
    EiswarnungConnectionError,
    EiswarnungConnectionTimeoutError,
    EiswarnungError,
)

from . import load_fixtures


async def test_json_request(
    aresponses: ResponsesMockServer, eiswarnung_client: Eiswarnung
) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "api.eiswarnung.de",
        "/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("forecast_type0.json"),
        ),
    )
    await eiswarnung_client._request("test")
    await eiswarnung_client.close()


async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "api.eiswarnung.de",
        "/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("forecast_type0.json"),
        ),
    )
    async with Eiswarnung(api_key="fake", latitude=42.1, longitude=11.1) as forecast:
        await forecast._request("test")


async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout from Eiswarnung API."""

    # Faking a timeout by sleeping
    async def response_handler(_: ClientResponse) -> Response:
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!",
            text=load_fixtures("forecast_type0.json"),
        )

    aresponses.add("api.eiswarnung.de", "/", "GET", response_handler)

    async with ClientSession() as session:
        client = Eiswarnung(
            api_key="fake",
            latitude=42.1,
            longitude=11.1,
            session=session,
            request_timeout=0.1,
        )
        with pytest.raises(EiswarnungConnectionTimeoutError):
            assert await client.forecast()


async def test_content_type(
    aresponses: ResponsesMockServer, eiswarnung_client: Eiswarnung
) -> None:
    """Test request content type error from Eiswarnung API."""
    aresponses.add(
        "api.eiswarnung.de",
        "/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "blabla/blabla"},
        ),
    )

    with pytest.raises(EiswarnungError):
        assert await eiswarnung_client._request("test")


async def test_client_error() -> None:
    """Test request client error from Eiswarnung API."""
    async with ClientSession() as session:
        client = Eiswarnung(
            api_key="fake",
            latitude=42.1,
            longitude=11.1,
            session=session,
        )
        with (
            patch.object(
                session,
                "request",
                side_effect=ClientError,
            ),
            pytest.raises(EiswarnungConnectionError),
        ):
            assert await client._request("test")
