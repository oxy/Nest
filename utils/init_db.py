'''
Module to initialize the database with the required data.
'''

import rethinkdb as r

def initialize(database='nest'):
    '''
    Initialize a database with required tables.
    Creates a database with a 'guilds' and 'users' table.

    Parameters
    ----------
    database: str
        Name of the database.
    '''
    conn = r.connect()
    r.db_create(database).run(conn)
    r.db('nest').table_create('guilds').run(conn)
    r.db('nest').table_create('users').run(conn)

if __name__ == '__main__':
    initialize()
