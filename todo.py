#!/usr/bin/env python

import collections
import click
import hashlib
import json
import os


ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, 'todos.json')
RENDER_ROOT = os.path.join(ROOT, 'todo')

TODO = 'todo'
DONE = 'done'


def _hash(todo):
    m = hashlib.md5()
    m.update(json.dumps(todo, sort_keys=True).encode())
    return m.hexdigest()


class Mgr(object):
    def __init__(self, data):
        self._data = data

    def list(self):
        return {
            k: v for k, v in self._data.items()
            if v.get('status', TODO) != DONE
        }

    def search(self, expr):
        return {k: v for k, v in self.list().items() if expr in v['short']}

    def set_done(self, todo_id):
        self._data[todo_id]['status'] = DONE
        self._journal()

    def add(self, short, notes=None):
        todo = {'short': short, 'status': TODO}
        if notes is not None:
            todo['notes'] = notes
        self._data[_hash(todo)] = todo
        self._journal()

    def _journal(self):
        with open(DB, 'w') as dbf:
            dbf.write(json.dumps(self._data))


def manager():
    data = {}
    if os.path.isfile(DB):
        with open(DB) as dbf:
            data = json.loads(dbf.read())
    return Mgr(data)


@click.group()
def cli():
    pass


@cli.command('list')
def list_em():
    print(manager().list())


@cli.command()
def render():
    if not os.path.isdir(RENDER_ROOT):
        os.makedirs(RENDER_ROOT)
    with open(os.path.join(RENDER_ROOT, 'README.md'), 'w') as readme:
        readme.write('TODO\n----\n')
        for todo in manager().list().values():
            readme.write('* {}\n'.format(todo['short']))
            if 'notes' in todo:
                readme.write('  * {}\n'.format(todo['notes']))


if __name__ == '__main__':
    cli()
