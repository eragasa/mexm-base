from abc import ABC
from typing import List
import os

class Task():
    def __init__(
        self,
        name: str,
        simulation_type: str,
        simulation_path: str,
        n_cores: int,
        n_nodes: int,
        required: List[str] = {}
    ):
        """

        Arguments:
            task_name (str): the name of the task
            simulation_type (str): the type of simulation
            simulation_path (str): the path to the simulation, will 
                be converted to an absolute path
            n_cores (int): the number of processor cores to use
            n_nodes (int): the number of processor nodes to use
            request (List[str]): a list of task_names that this 
                dependent upon
        """
        self.name = name
        self.simulation_type = simulation_type
        self._simulation_path = simulation_path
        self.n_cores = n_cores
        self.n_nodes = n_nodes
         

    @property
    def simulation_path(self):
        return self._simulation_path

    @simulation_path.setter
    def simulation_path(self, path):
        self._simulation_path = os.path.abspath(path)

class DbAdapter(ABC):
    def __init__(self, db_path: str = None):
        self.db_path = os.path.abspath(db_path)

class SqliteAdapter(DbAdapter):


import mysql.connector
class MysqlAdapter(DbAdapter):
    def __init__(
        self, 
        host="localhost",
        port=None,
        dbname="mexm"
        user="username", 
        password="password"
    ):
        del port, dbname # required definition by abstract class
                         # but not used 
        self.db_connector = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

import psycopg2
class PsqlAdapter(DbAdapter):
    def __init__(
        self,
        hostname='localhost',
        port=5432,
        dbname="mexm",
        user="username",
        password="password"
    ):
        self.db_conn=psycopg2.connect(
            self.get_sql_connection_string(
                hostname=hostname,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )
        )

    def get_sql_connection_string(
        self, 
        hostname,
        dbname,
        port, 
        user, 
        password
    ):
        str_connection = (
            "host={host} "
            "port={port} "
            "dbname={dbname} "
            "user={user} "
            "password={password}"
        ).format(
            host=hostname, 
            port=port, 
            dbname=dbname,
            user=user,
            password=password
        )
        return str_connection

        

class TaskManager(ABC):
    def __init__(self, sql_adapter: DbAdapter):
        self.task_repository = {}
        self.sql_adapter = sql_adapter


    def submit_task(self):
        pass


class SerialTaskManager(TaskManager): pass
class MpiTaskManager(TaskManager): pass
