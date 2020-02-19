import os
import time
import sqlite3

class JobOverlordDatabase():
    def __init__(self, mexm_sql_path=None):

        if mexm_sql_path is None:
            try:
                self.mexm_sqlite_path = os.environ['MEXM_SQLITE_PATH']
            except KeyError:
                self.mexm_sqlite_path = 'mexm.db'
        else:
            self.mexm_sqlite_path = mexm_sql_path

    def execute_command(self, sql_cmd, sql_values=None):
        conn = sqlite3.connect(self.mexm_sqlite_path)
        if values == None:
            conn.execute(sql_cmd)
        else:
            conn.execute(sql_cmd, sql_values)
        conn.commit()
        conn.close()

    def build_schema(self):
        conn = sqlite3.connect(self.mexm_sqlite_path)
        if self.check_if_table_exists(table_name='simulation_jobs'):
            conn.execute('DROP TABLE simulation_jobs')
        sql_command = (
            'CREATE TABLE simulation_jobs ('
            'job_id integer primary key autoincrement,\n'
            'job_name text not null,\n'
            'job_path text not null,\n'
            'timestamp_start text default current_timestamp,\n'
            'cluster_name text not null,\n'
            'cluster_job_id text,\n'
            'cluster_status text\n'
            ');'
        )


        # execute, commit to the database
        try:
            conn.execute(sql_command)
        except sqlite3.OperationalError:
            print(sql_command)
        conn.commit()

        # close the database
        conn.close()


    def create_new_simulation_job(self, 
                                  job_name, 
                                  job_path,
                                  cluster_name):
        sql_command = (
            'insert into simulation_jobs '
            '(job_name, job_path, cluster_name)'
            'VALUES'
            '(?,?,?);')

        sql_values = (
            job_name, 
            job_path,
            cluster_name
        )

        # connect, execute, commit, and close the database
        conn = sqlite3.connect(self.mexm_sqlite_path)
        conn.execute(sql_command, sql_values)
        conn.commit()
        conn.close()


    def check_if_table_exists(self, table_name):
        conn = sqlite3.connect(self.mexm_sqlite_path)
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        cursor = conn.execute(cmd.format(table_name=table_name))

        if len(cursor.fetchall()) == 0:
            return False
        else:
            return True
        print(len(cursor.fetchall()))
        
if __name__ == "__main__":
    o = JobOverlordDatabase()
    o.build_schema()
    o.create_new_simulation_job(job_name='name', job_path='path', cluster_name='pitzer')

    conn = sqlite3.connect(o.mexm_sqlite_path)
    cursor = conn.execute('SELECT * FROM simulation_jobs')

    for row in cursor:
        print(row)
    conn.close()
