import pytest

import os
from mexm.database import Sqlite3Adapter

@pytest.fixture
def dbpath():
    dbpath = "mexm.db"
    return dbpath

@pytest.fixture
def objDb(dbpath):
    return Sqlite3Adapter(dbpath)

def test_static__sqlstrings(objDb):
    assert isinstance(objDb.sqlstrings, dict)

def test_init__default(dbpath):
    objDb = Sqlite3Adapter(dbpath)
    assert os.path.isfile(dbpath)

if __name__ == "__main__":
    dbpath = "mexm.db"
    objDb = Sqlite3Adapter(dbpath)

