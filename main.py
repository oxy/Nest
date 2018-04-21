'''
Load and start the Nest client.
'''

import os
import logging

import yaml

from core import utils, client

DEFAULTS = {'prefix': {'user': 'nest$', 'mod': 'nest@', 'owner': 'nest#'},
            'database': 'nest'}

def main():
    '''
    Parse config from file or environment and launch bot.
    '''
    logger = logging.getLogger()
    if os.path.isfile('config.yml'):
        logger.debug('Found config, loading...')
        with open('config.yml') as file:
            config = yaml.safe_load(file)
    else:
        logger.debug('Config not found, trying to read from env...')
        env = {key[8:].lower(): val for key, val in os.environ.items()
               if key.startswith('NESTBOT_')}
        config = {'tokens': {}, 'settings': {}}

        for key, val in env.items():
            if key.startswith('token_'):
                config['tokens'][key[6:]] = val
            else:
                keys = key.split('_')
                pointer = utils.dictwalk(
                    dictionary=config['settings'],
                    tree=keys[:-1],
                    fill=True)

                pointer[keys[-1]] = val

    settings = {**DEFAULTS, **config['settings']}

    bot = client.NestClient(settings)

    for module in os.listdir('modules'):
        # Ignore hidden directories
        if not module.startswith('.'):
            bot.load_module(module)

    bot.run(config['tokens']['discord'])


if __name__ == '__main__':
    main()
