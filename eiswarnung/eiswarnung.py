"""Asynchronous Python client for the Eiswarnung API."""
from __future__ import annotations

import asyncio
import socket
from collections.abc import Mapping
from dataclasses import dataclass
from importlib import metadata
from typing import Any

import async_timeout
from aiohttp.client import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import (
    EiswarnungConnectionError,
    EiswarnungError,
    EiswarnungRatelimitError,
    EiswarnungRequestError,
)
from .models import Forecast, Ratelimit


@dataclass
class Eiswarnung:
    """Main class for handling connections with the Eiswarnung API."""

    api_key: str
    latitude: float
    longitude: float

    request_timeout: float = 10.0
    session: ClientSession | None = None
    ratelimit: Ratelimit | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """Handle a request to the Eiswarnung API.

        A generic method for sending/handling HTTP requests done against
        the Eiswarnung API.

        Args:
            uri: Request URI, without '/', for example, 'status'.
            method: HTTP method to use.
            params: Dictionary of parameters to send to the Eiswarnung API.

        Returns:
            The response data from the Eiswarnung API.

        Raises:
            EiswarnungRequestError: There is something wrong with the
                variables used in the request.
            EiswarnungConnectionError: An error occurred while communicating
                with the Eiswarnung API.
            EiswarnungError: Received an unexpected response from the
                Eiswarnung API.
            EiswarnungRatelimitError: The number of requests has exceeded
                the rate limit of the Eiswarnung API.
        """
        version = metadata.version(__package__)
        url = URL.build(scheme="https", host="api.eiswarnung.de", path="/").join(
            URL(uri)
        )

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonEiswarnung/{version}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise EiswarnungConnectionError(
                "Timeout occurred while connecting to Eiswarnung API"
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            raise EiswarnungConnectionError(
                "Error occurred while communicating with Eiswarnung API"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise EiswarnungError(
                "Unexpected response from the Eiswarnung API",
                {"Content-Type": content_type, "response": text},
            )

        data = await response.json()
        if data["code"] == 200:
            self.ratelimit = Ratelimit.from_response(data)

        if data["code"] in [300, 400, 401]:
            raise EiswarnungRequestError(data)

        if data["code"] == 402:
            raise EiswarnungRatelimitError(data)

        return data

    async def forecast(self) -> Forecast:
        """Get forecast information from the Eiswarnung API.

        Returns:
            A Forecast object, with a ice warning forecast.
        """
        data = await self._request(
            "/",
            params={
                "key": self.api_key,
                "lat": self.latitude,
                "lng": self.longitude,
            },
        )
        return Forecast.from_response(data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Eiswarnung:
        """Async enter.

        Returns:
            The Eiswarnung object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
