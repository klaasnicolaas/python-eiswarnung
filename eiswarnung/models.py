"""Data models for the Eiswarnung API."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class ForecastType(str, Enum):
    """Enumeration representing the Eiswarnung Forecast type."""

    NO_ICE = "No ice"
    POSSIBLY_ICE = "Possibly ice"
    ICE = "Ice"


@dataclass
class Estimate:
    """Object representing an Estimate response from Eiswarnung."""

    request_date: datetime
    status_id: int
    forecast_text: str
    forecast_city: str
    forecast_date: datetime

    @property
    def forecast_type(self) -> ForecastType:
        """Return API account_type information.

        Returns:
            The forecast type.
        """
        if self.status_id == 1:
            return ForecastType.ICE
        if self.status_id == 2:
            return ForecastType.POSSIBLY_ICE
        return ForecastType.NO_ICE

    @classmethod
    def from_response(cls, data: dict) -> Estimate:
        """Create an Estimate from a response.

        Args:
            data: The response data from the Eiswarnung API.

        Returns:
            A Estimate object.
        """
        data = data["result"]
        return Estimate(
            request_date=datetime.strptime(
                data.get("requestDate"), "%Y-%m-%d %H:%M:%S"
            ),
            status_id=data.get("forecastId"),
            forecast_text=data.get("forecastText").replace(".", ""),
            forecast_city=data.get("forecastCity"),
            forecast_date=datetime.strptime(
                data.get("forecastDate"), "%Y-%m-%d"
            ).date(),
        )


@dataclass
class Ratelimit:
    """Information about the current rate limit."""

    call_limit: int
    remaining_calls: int
    retry_after: int

    @classmethod
    def from_response(cls, data: dict[str, Any]) -> Ratelimit:
        """Create a Ratelimit object from the response data.

        Args:
            data: The response data from the Eiswarnung API.

        Returns:
            A Ratelimit object.
        """
        return cls(
            call_limit=data.get("callsDailyLimit"),
            remaining_calls=data.get("callsLeft"),
            retry_after=data.get("callsResetInSeconds"),
        )
