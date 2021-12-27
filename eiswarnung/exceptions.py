"""Exceptions for Eiswarnung API."""


class EiswarnungError(Exception):
    """General Eiswarnung exception."""


class EiswarnungConnectionError(EiswarnungError):
    """Eiswarnung connection exception."""


class EiswarnungRequestError(EiswarnungError):
    """Eiswarnung wrong request input variables."""

    def __init__(self, data: dict) -> None:
        """Init a solar request error.

        Args:
            data: The data that caused the error.

        https://www.eiswarnung.de/rest-api/
        """
        super().__init__(f'{data["message"]} (error {data["code"]})')
        self.code = data["code"]


class EiswarnungRatelimitError(EiswarnungError):
    """Eiswarnung ratelimit exception."""

    def __init__(self, data: dict) -> None:
        """Init a rate limit error.

        Args:
            data: The data that caused the error.
        """
        super().__init__(f'{data["message"]} (error {data["code"]})')
        self.code = data["code"]
