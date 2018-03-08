#!/usr/bin/env python

import json
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))


class Mgr(object):
    def __init__(self, db, data):
        self._db = db
        self._data = data

    def list(self):
        return self._data

    def add(self, short, notes=None):
        todo = {'short': short}
        if notes is not None:
            todo['notes'] = notes
        self._data.append(todo)
        with open(self._db, 'w') as dbf:
            dbf.write(json.dumps(self._data))


def manager(db=None):
    if db is None:
        db = os.path.join(DIR, 'todos.json')

    data = []
    if os.path.isfile(db):
        with open(db) as dbf:
            data = json.loads(dbf.read())
    return Mgr(db, data)


def main(argv):
    mgr = manager()
    print(mgr.list())


if __name__ == '__main__':
    main(sys.argv)
