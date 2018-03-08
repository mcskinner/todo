#!/usr/bin/env python

import hashlib
import json
import os
import sys


DIR = os.path.dirname(os.path.abspath(__file__))

TODO = 'todo'
DONE = 'done'


def _hash(todo):
    m = hashlib.md5()
    m.update(json.dumps(todo, sort_keys=True).encode())
    return m.hexdigest()


class Mgr(object):
    def __init__(self, db, data):
        self._db = db
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
        with open(self._db, 'w') as dbf:
            dbf.write(json.dumps(self._data))


def manager(db=None):
    if db is None:
        db = os.path.join(DIR, 'todos.json')

    data = {}
    if os.path.isfile(db):
        with open(db) as dbf:
            data = json.loads(dbf.read())
    return Mgr(db, data)


def main(argv):
    mgr = manager()
    print(mgr.list())


if __name__ == '__main__':
    main(sys.argv)
