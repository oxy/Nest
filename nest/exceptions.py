"""
Exceptions raised by the nest client and modules.
"""

from discord import ClientException


class MissingFeatures(ClientException):
    """
    Called when a module requires a feature not present in the client.
    """

    def __init__(self, cog, features: set):
        self.features = features
        self.cog = cog
        super().__init__(
            f"{cog.__class__.__name__} requires missing features: {features}"
        )


class WebAPIException(Exception):
    """
    Base exception from which API exceptions are derived.
    """

    def __init__(self, api):
        super().__init__()
        self.api = api


class WebAPINoResults(WebAPIException):
    """
    Raised when an API does not return a result.
    """
    pass


class WebAPIUnreachable(WebAPIException):
    """
    Raised when a web API could not be reached.
    """
    pass


class WebAPIInvalidResponse(WebAPIException):
    """
    Raised when a web API returns an invalid response.
    """

    def __init__(self, api, status):
        super().__init__(api)
        self.status = status
