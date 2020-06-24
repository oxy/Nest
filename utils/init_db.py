"""
Module to initialize the database with the required tables.
"""

import asyncio
import os
import asyncpg
import yaml

SQL_QUERY = "ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {field} {ftype};"
SQL_TABLECREATE = "CREATE TABLE IF NOT EXISTS {table} (id BIGINT PRIMARY KEY);"


def buildqueries():
    """
    Load fields and types from module configurations and build database queries.
    """
    data = {}
    queries = []

    # Fetch all queries.
    for module in os.listdir("modules"):
        if not module.startswith("."):
            path = os.path.join("modules", module, "db.yml")
            if not os.path.exists(path):
                continue
            with open(path) as dbdata:
                module = yaml.load(dbdata)
                for table, fields in module.items():
                    if table in data.keys():
                        data[table].update(fields)
                    else:
                        data[table] = fields

    for table in data:
        queries.append(SQL_TABLECREATE.format(table=table))

    for table, fields in data.items():
        for field, ftype in fields.items():
            queries.append(
                SQL_QUERY.format(table=table, field=field, ftype=ftype)
            )

    return queries


async def runqueries(*queries: str):
    """
    Run all database queries using asyncpg.
    """
    pool = await asyncpg.create_pool(database="nest")

    async with pool.acquire() as conn:
        for query in queries:
            await conn.execute(query)


def main():
    """
    Run as a script.
    """
    queries = buildqueries()
    print("Queries are: ", *queries, sep="\n")

    choice = input("Continue? [y/n]: ")
    if choice.lower() == "y":
        print("Running queries on database...")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(runqueries(*queries))
    else:
        print("Exiting.")


if __name__ == "__main__":
    main()
