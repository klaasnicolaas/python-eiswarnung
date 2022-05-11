# pylint: disable=W0621
"""Asynchronous Python client for the Eiswarnung API."""

import asyncio

from eiswarnung import Eiswarnung, Forecast


async def main() -> None:
    """Test."""
    async with Eiswarnung(
        api_key="API_KEY",
        latitude=49.41,
        longitude=8.68,
    ) as client:
        forecast: Forecast = await client.forecast()
        print("--- FORECAST ---")
        print(forecast)
        print(f"Forecast Type: {forecast.forecast_type}")
        print(f"Forecast Text: {forecast.text}")
        print(f"Forecast Date: {forecast.forecast_date}")
        print(f"Forecast City: {forecast.city}")
        print()
        print(f"Request Date: {forecast.request_date}")
        print()
        print("--- RATE LIMIT ---")
        print(client.ratelimit)


if __name__ == "__main__":
    asyncio.run(main())
