"""Basic tests for the Eiswarnung API."""
# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from eiswarnung import (
    Eiswarnung,
    EiswarnungConnectionError,
    EiswarnungError,
    EiswarnungRatelimitError,
    EiswarnungRequestError,
)

from . import load_fixtures


@pytest.mark.asyncio
async def test_json_request(aresponses):
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
    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        )
        response = await client._request("test")
        assert response is not None
        await client.close()


@pytest.mark.asyncio
async def test_internal_session(aresponses):
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


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from Eiswarnung API."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!", text=load_fixtures("forecast_type0.json")
        )

    aresponses.add("api.eiswarnung.de", "/", "GET", response_handler)

    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake",
            latitude=42.1,
            longitude=11.1,
            session=session,
            request_timeout=0.1,
        )
        with pytest.raises(EiswarnungConnectionError):
            assert await client.estimate()


@pytest.mark.asyncio
async def test_content_type(aresponses):
    """Test request content type error from Eiswarnung API."""
    aresponses.add(
        "api.eiswarnung.de",
        "/",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "blabla/blabla"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        )
        with pytest.raises(EiswarnungError):
            assert await client.estimate()


@pytest.mark.asyncio
async def test_client_error():
    """Test request client error from Eiswarnung API."""
    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        )
        with patch.object(
            session, "request", side_effect=aiohttp.ClientError
        ), pytest.raises(EiswarnungConnectionError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_http_error401(aresponses):
    """Test HTTP 401 response handling."""
    aresponses.add(
        "api.eiswarnung.de",
        "/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("status_401.json"),
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        )
        with pytest.raises(EiswarnungRequestError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_http_error402(aresponses):
    """Test HTTP 402 response handling."""
    aresponses.add(
        "api.eiswarnung.de",
        "/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("status_402.json"),
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        )
        with pytest.raises(EiswarnungRatelimitError):
            assert await client._request("test")
