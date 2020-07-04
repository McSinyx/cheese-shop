#!/usr/bin/env python3
from json import JSONDecodeError
from typing import Any, Awaitable, Dict, Iterable, List

from asks.sessions import Session
from mysql.connector import connect
from trio import Nursery, open_nursery, run
from trove_classifiers import classifiers

USER = 'wensleydale'
DB = 'cheese_shop'
INDEX = 'https://pypi.org'
CONNECTIONS = 20


class CheeseMaker:
    """Cheese maker for Mr Wensleydale's cheese shop."""

    def __init__(self, nursery: Nursery, session: Session) -> None:
        self.nursery, self.session = nursery, session
        self.connection = connect(user=USER, database=DB)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.classifiers = {}
        for classifier in classifiers:
            self.insert('troves', classifier=classifier)
            self.classifiers[classifier] = self.cursor.lastrowid

    def start_soon(self, async_fn: Awaitable, *args: Any) -> None:
        """Creates a child task, scheduling await async_fn(*args)."""
        self.nursery.start_soon(async_fn, *args)

    def insert(self, table: str, **kwargs: str) -> None:
        """Insert items into the given table."""
        items = {k: v for k, v in kwargs.items() if v is not None}
        self.cursor.execute(
            f'INSERT IGNORE INTO {table} ({", ".join(items)}) '
            f'VALUES ({", ".join(map(repr, items.values()))})')

    def insert_info(self, release_id: int, info: Dict[str, Any]) -> None:
        """Insert auxiliary information of the given release."""
        self.insert('contacts', name=info['author'],
                    email=info['author_email'])
        self.insert('information', release_id=release_id,
                    summary=info['summary'], homepage=info['home_page'],
                    email=info['author_email'])
        for classifier in info['classifiers']:
            self.insert('classifiers', release_id=release_id,
                        trove_id=self.classifiers[classifier])
        for keyword in (info['keywords'] or '').split(','):
            self.insert('keywords', release_id=release_id, term=keyword)
        for dep in (info['requires_dist'] or []):
            self.insert('dependencies', release_id=release_id, dependency=dep)

    def insert_dist(self, release_id: int,
                    distributions: List[Dict[str, Any]]) -> None:
        """Insert distribution information of the given release."""
        for dist in distributions:
            self.insert('distributions', release_id=release_id,
                        filename=dist['filename'], size=dist['size'],
                        url=dist['url'], dist_type=dist['packagetype'],
                        python_version=dist['python_version'],
                        requires_python=dist['requires_python'],
                        sha256=dist['digests']['sha256'],
                        md5=dist['digests']['md5'])

    async def json(self, path: str) -> Any:
        """Return the JSON response to the given GET request."""
        response = await self.session.get(
            path=path, headers={'Accept': 'application/json'})
        return response.json()

    async def culture(self) -> Iterable[str]:
        """Return the 100 most popular cheeses in cheese shop."""
        stats = await self.json('/stats')
        return stats['top_packages'].keys()

    async def drain(self, project_name: str, version: str) -> None:
        """Fetch metadata of the given distribution."""
        try:
            content = await self.json(f'/pypi/{project_name}/{version}/json')
        except JSONDecodeError:
            return
        print('Processing', project_name, version)
        self.insert('releases', project=project_name, version=version)
        release_id = self.cursor.lastrowid
        self.insert_info(release_id, content['info'])
        self.insert_dist(release_id, content['urls'])

    async def coagulate(self, project_name: str) -> None:
        """Fetch project's available versions and metadata."""
        content = await self.json(f'/pypi/{project_name}/json')
        print('Fetching', project_name)
        for version in content['releases'].keys():
            # Recklessly filter out prereleases
            for n in version.split('.'):
                try:
                    int(n)
                except ValueError:
                    break
            else:
                self.start_soon(self.drain, project_name, version)


async def main():
    """Make cheeses."""
    async with open_nursery() as nursery:
        maker = CheeseMaker(nursery, Session(INDEX, connections=CONNECTIONS))
        for project_name in await maker.culture():
            maker.start_soon(maker.coagulate, project_name)


if __name__ == '__main__': run(main)
