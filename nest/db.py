'''Store and retrieve user-specific info'''
import functools
import rethinkdb as r

r.set_loop_type("asyncio")


def db_method(func):
    '''Add a few checks and conversions before running a database operation.

    Parameters
    ----------
    func: func
        Function to wrap.
    '''
    @functools.wraps(func)
    async def inner(cls, **kwargs):
        '''
        Inner function to add checks.
        '''
        if not cls.connection.is_open():
            await cls.connection.reconnect()

        if not isinstance(kwargs['table'], r.RqlQuery):
            kwargs['table'] = cls.database.table(kwargs['table'])

        if not isinstance(kwargs['itemid'], str):
            kwargs['itemid'] = str(kwargs['itemid'])

        return await func(cls, **kwargs)
    return inner


class DBWrapper:
    '''Store and retrieve info from a RethinkDB database.

    Attributes
    ----------
    database:
        Reference to the RethinkDB database used.
    '''

    def __init__(self, database: str,
                 connection: r.Connection):
        self.connection = connection
        self.database = r.db(database)

    @db_method
    async def read(self, *, table, itemid: str, item=None):
        '''|coro|

        Read entry from database and return induvidual item.

        Attributes
        ----------
        table:
            Name of the table to query.
        itemid:
            Snowflake of the entry to search for.
        item: str
            Name of the item to return, if any.
        '''
        query = table.filter(r.row['id'] == itemid).limit(1)
        cursor = await query.run(self.connection)
        try:
            document = await cursor.next()
            if item is None:
                data = document
            else:
                data = document[item]
        except (KeyError, TypeError, r.errors.ReqlCursorEmpty):
            data = None
        return data

    @db_method
    async def write(self, *, table, itemid: str, item, data):
        '''|coro|

        Write data for an item to a database.

        Attributes
        ----------
        table:
            Name of the table to query.
        itemid:
            Snowflake of the entry to update.
        item: str
            Name of the item to write to.
        data:
            Data to write to the item.
        '''
        if await self.read(table=table, itemid=itemid) is not None:
            row = table.filter(r.row['id'] == itemid).limit(1)
            await row.update({item: data}).run(self.connection)
        else:
            query = table.insert([{'id': itemid, item: data}])
            await query.run(self.connection)


class ItemWrapper:
    '''Store and retrieve information for an item.

    Attributes
    ----------
    table: str
        Name of the table where the item is located.
    item: str
        Item to read from/write to.
    '''

    def __init__(self, wrapper: DBWrapper, table: str, item: str):
        self._wrapper = wrapper
        self.table = wrapper.database.table(table)
        self.item = item

    def read(self, itemid: str):
        '''|coro|

        Reads a single item and returns it.

        Attributes
        ----------
        itemid: str
            Snowflake to search for.
        '''
        return self._wrapper.read(
            table=self.table, item=self.item, itemid=itemid)

    def write(self, itemid: str, data):
        '''|coro|

        Writes data for an item to the database.

        Attributes
        ----------
        itemid: str
            Snowflake to write to.
        data:
            Data to write.
        '''
        return self._wrapper.write(
            table=self.table, item=self.item, itemid=itemid, data=data)
