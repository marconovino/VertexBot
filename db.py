from asyncpg import create_pool
from os import getenv

CREATE = """CREATE TABLE IF NOT EXISTS Versions (
  versionid VARCHAR(65535),
  versiondownload VARCHAR(65535)
);"""

class Database:
    """A database interface for the bot to connect to Postgres."""

    def __init__(self):
        self.pool = None

    async def setup(self):
        self.pool = await create_pool(dsn=getenv("DATABASE_URL"))
        await self.execute(CREATE)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            await conn.execute(query, *args)

    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def create_version_link(self, versionID: str, versionLink: str):
        return await self.fetchrow("INSERT INTO Versions (versionid, versiondownload) VALUES ($1, $2) RETURNING *;", versionID, versionLink)

    async def update_version_link(self, newlink: str, versionID: str):
        return await self.execute("UPDATE Versions SET versiondownload = $1 WHERE versionid = $2;", newlink, versionID)
        
    async def get_version_link(self, versionID: str):
        return await self.fetchrow("SELECT * FROM Versions WHERE versionid = $1;", versionID)

    async def get_all_versions(self):
        return await self.fetch("SELECT * FROM Versions")
