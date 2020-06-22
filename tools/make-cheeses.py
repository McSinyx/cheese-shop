#!/usr/bin/env python3
from typing import KeysView

from asks.sessions import Session
from trio import Nursery, open_nursery, run

PYPI = 'https://pypi.org'
CONNECTIONS = 20


async def culture(session: Session) -> KeysView[str]:
    """Return the 100 most popular cheeses in cheese shop."""
    stats = await session.get(
        path='/stats', headers={'Accept': 'application/json'})
    return stats.json()['top_packages'].keys()


async def drain(project_name: str, version: str, session: Session) -> None:
    """Fetch metadata of the given distribution."""
    # XXX: insert the fetched metadata to a database
    await session.get(path=f'/pypi/{project_name}/{version}/json')
    print(project_name, version)


async def coagulate(project_name: str, nursery: Nursery,
                    session: Session) -> None:
    """Fetch project's available versions and the metadata of each."""
    response = await session.get(path=f'/pypi/{project_name}/json')
    for version in response.json()['releases'].keys():
        # Recklessly filter out prereleases
        for n in version.split('.'):
            try:
                int(n)
            except ValueError:
                break
        else:
            nursery.start_soon(drain, project_name, version, session)


async def main(session: Session):
    """Make cheeses."""
    async with open_nursery() as nursery:
        for project_name in await culture(session):
            nursery.start_soon(coagulate, project_name, nursery, session)


if __name__ == '__main__':
    run(main, Session(PYPI, connections=CONNECTIONS))
