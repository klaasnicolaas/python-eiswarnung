"""Test the exceptions of Eiswarnung."""

# pylint: disable=protected-access
import pytest
from aresponses import ResponsesMockServer

from eiswarnung import (
    Eiswarnung,
    EiswarnungRatelimitError,
    EiswarnungRequestError,
)

from . import load_fixtures


async def test_http_error401(
    aresponses: ResponsesMockServer, eiswarnung_client: Eiswarnung
) -> None:
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
    with pytest.raises(EiswarnungRequestError):
        assert await eiswarnung_client._request("test")


async def test_http_error402(
    aresponses: ResponsesMockServer, eiswarnung_client: Eiswarnung
) -> None:
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
    with pytest.raises(EiswarnungRatelimitError):
        assert await eiswarnung_client._request("test")
