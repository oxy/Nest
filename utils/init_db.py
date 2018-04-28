'''
Module to initialize the database with the required tables.
'''

import asyncio
import asyncpg

QUERIES = ['''
    CREATE TABLE prefix(
        id numeric(21, 0) PRIMARY KEY,
        user_prefix text,
        mod_prefix text
    )
    ''',
    '''
    CREATE TABLE locale(
        id numeric(21, 0) PRIMARY KEY,
        locale text
    );
    ''']

async def initialize(database):
    conn = await asyncpg.connect(database=database)
    # TODO: Read configuration data from modules.
    for query in QUERIES:
        await conn.execute(query)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize('nest'))
