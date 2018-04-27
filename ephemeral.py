'''
Load and start the Nest client.
'''

import os
import logging

import yaml

from nest import client

DEFAULTS = {'prefix': {'user': 'nest$', 'mod': 'nest@', 'owner': 'nest#'},
            'database': 'nest', 'locale': 'en_US'}

def main():
    '''
    Parse config from file and launch bot without a database connection.
    '''
    with open('config.yml') as file:
        config = yaml.safe_load(file)

    settings = {**DEFAULTS, **config['settings']}
    prefixes = config['settings'].get('prefix', DEFAULTS['prefix'])
    locale = config['settings'].get('locale', DEFAULTS['locale'])

    bot = client.NestClient(
        locale=locale,
        prefix=prefixes,
        owners=settings['owners'])

    for module in os.listdir('modules'):
        # Ignore hidden directories
        if not module.startswith('.'):
            bot.load_module(module)

    bot.run(config['tokens']['discord'])


if __name__ == '__main__':
    main()
