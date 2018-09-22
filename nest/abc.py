"""Provides abstract base classes for certain functionality."""

import abc
from discord.ext import commands


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
    async def get(self, ctx: commands.Context):
        """
        Gets data for a specific context.

        Parameters
        ----------
        ctx: commands.Context
            Context to get data for.
        Returns
        -------
        Data for the given context.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def set(self, ctx: commands.Context, data):
        """
        Sets data for a specific context.

        Parameters
        ----------
        ctx: commands.Context
            Context to set data for.
        data:
            Data to set.
        """
        raise NotImplementedError
