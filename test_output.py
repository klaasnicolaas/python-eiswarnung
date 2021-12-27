# pylint: disable=W0621
"""Asynchronous Python client for the Eiswarnung API."""

import asyncio

from eiswarnung import Eiswarnung, Estimate


async def main():
    """Test."""
    async with Eiswarnung(
        api_key="API_KEY",
        latitude=49.41,
        longitude=8.68,
    ) as client:
        estimate: Estimate = await client.estimate()
        print("--- ESTIMATE ---")
        print(estimate)
        print(f"Forecast Type: {estimate.forecast_type}")
        print(f"Forecast Text: {estimate.forecast_text}")
        print(f"Forecast Date: {estimate.forecast_date}")
        print(f"Forecast City: {estimate.forecast_city}")
        print()
        print(f"Request Date: {estimate.request_date}")
        print()
        print("--- RATE LIMIT ---")
        print(client.ratelimit)
        print(f"Call Limit: {client.ratelimit.call_limit}")
        print(f"Remaining Calls: {client.ratelimit.remaining_calls}")
        print(f"Retry After: {client.ratelimit.retry_after}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
