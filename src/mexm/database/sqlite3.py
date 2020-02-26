import os
import sqlite3
from mexm.database import DatabaseAdaptor

__all__ = ['Sqlite3Adapter']
class Sqlite3Adapter(DatabaseAdapter):
    def __init__(
        self,
        hostname=None,
        port=None,
        dbname="mexm.db",
        user=None,
        password=None
    ):
        # the following arguments are not used
        # but they must be defined for the abstract class
        self.db_conn = sqlite3.connect(
            os.path.abspath(dbname)
        )