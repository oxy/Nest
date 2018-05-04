"""
Module to initialize the database with the required tables.
"""

import asyncio
import os
import asyncpg


async def initialize(database):
    queries = []

    # Fetch all queries.
    for module in os.listdir("modules"):
        path = os.path.join("modules", module, "init.pgsql")
        if not module.startswith(".") and os.path.exists(path):
            with open(path) as query:
                queries.append(query.read())

    # Execute each query.
    conn = await asyncpg.connect(database=database)
    for query in queries:
        await conn.execute(query)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize("nest"))
