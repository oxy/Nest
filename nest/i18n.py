'''
Implement internationalization on a per-module level.
'''
import json
import logging
import os
from typing import Dict

from nest.helpers import dictwalk

class I18n:
    '''Internationalization functions for Nest.

    Attributes
    ----------
    locale: str
        Default locale.
    '''
    def __init__(self, locale: str):
        self._i18n_data = {}
        self._logger = logging.getLogger('nest.i18n')
        self.locale = locale
        self.load_locales()

    def load_locales(self):
        '''Load core data about each supported locale.'''
        directory = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(directory, 'i18n.json')

        with open(path) as datafile:
            data = json.load(datafile)

        for lang, lang_data in data.items():
            if lang not in self._i18n_data:
                self._logger.debug(f'Registering lang {lang}')
                self._i18n_data[lang] = {}

            self._i18n_data[lang].update(lang_data)

    def locales(self, current_locale: str) -> Dict[str, str]:
        '''Return dictionary of language data.

        Parameters
        ----------
        current_locale: str
            Locale to use (truncated to first two characters)
        '''

        locales = {}
        current_lang = current_locale[:2]
        for locale, data in self._i18n_data.items():
            lang = locale[:2]
            try:
                l_user = data['names'].get(
                    current_lang,
                    data['names'].get(self.lang))

                l_native = data['names'].get(lang)
                locales[locale] = {'user': l_user, 'native': l_native}
            except (KeyError, ValueError):
                self._logger.warning(f'{locale} has no name data! Ignoring.')
                continue
        return locales

    def load_module(self, module):
        '''Load language data for a module.

        Parameters
        ----------
        module: str
            Module to load from.
            Must be a valid module located in the modules/ directory.
        '''
        path = os.path.join('modules', module, 'i18n')

        if not os.path.exists(path):
            return

        for filename in os.listdir(path):
            if not filename.endswith('.json'):
                self._logger.warning(f'Ignoring {filename}!')
                continue

            locale = filename[:-5]

            if locale not in self._i18n_data:
                self._logger.debug(f'Creating locale {locale}.')
                self._i18n_data[locale] = {}

            with open(f'{path}/{filename}') as file:
                self._i18n_data[locale].update(json.load(file))

    def getstr(self, string: str, *, locale: str, cog: str):
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

    @property
    def lang(self):
        '''Default language.'''
        return self.locale[:2]

    def is_locale(self, locale: str):
        '''Check if given locale is valid.'''
        return locale in self._i18n_data.keys()
