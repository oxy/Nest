"""Provides abstract base classes for certain functionality."""

import abc

class Provider(abc.ABC):
    """
    Abstract base class for a provider.

    Attributes
    ----------
    provides: str
        Data the provider provides.

    Methods
    -------
    get:
        Fetches data 
    """
    provides: str

    @abc.abstractmethod
    async def get(self, ctx):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def set(self, ctx, data):
        raise NotImplementedError
