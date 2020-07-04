#!/usr/bin/env python3
from typing import Any, Awaitable, KeysView

from asks.sessions import Session
from mysql.connector import connect
from trio import Nursery, open_nursery, run

USER = 'wensleydale'
DB = 'cheese_shop'
INDEX = 'https://pypi.org'
CONNECTIONS = 20


class CheeseMaker:
    def __init__(self, nursery: Nursery, session: Session) -> None:
        self.nursery, self.session = nursery, session
        self.cursor = connect(user=USER, database=DB).cursor()

    def start_soon(self, async_fn: Awaitable, *args: Any) -> None:
        """Creates a child task, scheduling await async_fn(*args)."""
        self.nursery.start_soon(async_fn, *args)

    async def json(self, path: str) -> Any:
        """Return the JSON response to the given GET request."""
        response = await self.session.get(
            path=path, headers={'Accept': 'application/json'})
        return response.json()

    async def culture(self) -> KeysView[str]:
        """Return the 100 most popular cheeses in cheese shop."""
        stats = await self.json('/stats')
        return stats['top_packages'].keys()

    async def drain(self, project_name: str, version: str) -> None:
        """Fetch metadata of the given distribution."""
        # XXX: insert the fetched metadata to a database
        await self.json(f'/pypi/{project_name}/{version}/json')
        print(project_name, version)

    async def coagulate(self, project_name: str) -> None:
        """Fetch project's available versions and metadata."""
        response = await self.json(f'/pypi/{project_name}/json')
        for version in response['releases'].keys():
            # Recklessly filter out prereleases
            for n in version.split('.'):
                try:
                    int(n)
                except ValueError:
                    break
            else:
                self.start_soon(self.drain, project_name, version)


async def main(session: Session):
    """Make cheeses."""
    async with open_nursery() as nursery:
        maker = CheeseMaker(nursery, session)
        for project_name in await maker.culture():
            maker.start_soon(maker.coagulate, project_name)


if __name__ == '__main__':
    run(main, Session(INDEX, connections=CONNECTIONS))
