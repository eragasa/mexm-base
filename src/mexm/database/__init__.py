import os
from abc import ABC
class DatabaseAdapter(ABC):
    def __init__(self, dbpath: str = None):
        self.db_path = os.path.abspath(db_path)

from mexm.database.sqlite3 import Sqlite3Adapter

