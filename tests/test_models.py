"""Test the models."""

from aresponses import ResponsesMockServer

from eiswarnung import Eiswarnung, Forecast

from . import load_fixtures


async def test_forecast_type0(
    aresponses: ResponsesMockServer, eiswarnung_client: Eiswarnung
) -> None:
    """Test request for Forecast object."""
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
    forecast: Forecast = await eiswarnung_client.forecast()
    assert forecast.city == "Heidelberg"
    assert forecast.status_id == 0
    assert forecast.forecast_type == "No ice"


async def test_forecast_type1(
    aresponses: ResponsesMockServer, eiswarnung_client: Eiswarnung
) -> None:
    """Test request for Forecast object."""
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
    forecast: Forecast = await eiswarnung_client.forecast()
    assert forecast.city == "Heidelberg"
    assert forecast.status_id == 1
    assert forecast.forecast_type == "Ice"


async def test_forecast_type2(
    aresponses: ResponsesMockServer, eiswarnung_client: Eiswarnung
) -> None:
    """Test request for Forecast object."""
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
    forecast: Forecast = await eiswarnung_client.forecast()
    assert forecast.city == "Heidelberg"
    assert forecast.status_id == 2
    assert forecast.forecast_type == "Possibly ice"
