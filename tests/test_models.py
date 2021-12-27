"""Test the models."""
import aiohttp
import pytest

from eiswarnung import Eiswarnung, Estimate

from . import load_fixtures


@pytest.mark.asyncio
async def test_estimate_type0(aresponses):
    """Test request for Estimate object."""
    aresponses.add(
        "api.eiswarnung.de",
        "/",
        "GET",
        aresponses.Response(
            text=load_fixtures("forecast_type0.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        )
        estimate: Estimate = await client.estimate()
        assert estimate.forecast_city == "Heidelberg"
        assert estimate.status_id == 0
        assert estimate.forecast_type == "No ice"


@pytest.mark.asyncio
async def test_estimate_type1(aresponses):
    """Test request for Estimate object."""
    aresponses.add(
        "api.eiswarnung.de",
        "/",
        "GET",
        aresponses.Response(
            text=load_fixtures("forecast_type1.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        )
        estimate: Estimate = await client.estimate()
        assert estimate.forecast_city == "Heidelberg"
        assert estimate.status_id == 1
        assert estimate.forecast_type == "Ice"


@pytest.mark.asyncio
async def test_estimate_type2(aresponses):
    """Test request for Estimate object."""
    aresponses.add(
        "api.eiswarnung.de",
        "/",
        "GET",
        aresponses.Response(
            text=load_fixtures("forecast_type2.json"),
            status=200,
            headers={"Content-Type": "application/json"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Eiswarnung(
            api_key="fake", latitude=42.1, longitude=11.1, session=session
        )
        estimate: Estimate = await client.estimate()
        assert estimate.forecast_city == "Heidelberg"
        assert estimate.status_id == 2
        assert estimate.forecast_type == "Possibly ice"
