'''
Implement internationalization on a per-module level.
'''
import json
import logging
import os

from core.utils import dictwalk

class I18n:
    '''Internationalization functions for Nest.

    Attributes
    ----------
    locale: str
        Default locale to use if a string is not present in the given locale.
    '''
    def __init__(self, locale: str):
        self._i18n_data = {}
        self._logger = logging.getLogger('core.i18n')
        self.locale = locale

    def load_module(self, module):
        '''Load language data for a module.

        Parameters
        ----------
        module: str
            Module to load from.
            Must be a valid module located in the modules/ directory.
        '''
        path = f'modules/{module}/i18n'

        if not os.path.exists(path):
            return

        self._i18n_data[module] = {}

        for filename in os.listdir(path):
            if not filename.endswith('.json'):
                continue
            locale = filename[:-5]

            if locale not in self._i18n_data:
                self._logger.debug(f'Creating locale {locale}.')
                self._i18n_data[locale] = {}

            with open(f'{path}/{filename}') as file:
                self._i18n_data[locale].update(json.load(file))

    def getstr(self, string: str, locale: str, cog: str):
        '''Get a localized string.

        Parameters
        ----------
        string: str
            Internal name of translated string.
        locale: str
            Locale to use, defaults to en_US if data not present.
        cog: str
            Cog to search for string.
        '''
        try:
            item = dictwalk(self._i18n_data, [locale, cog, string])
        except ValueError:
            try:
                item = dictwalk(self._i18n_data, [self.locale, cog, string])
            except ValueError:
                item = string
        return item
