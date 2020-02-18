import os
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

    def execute_command(self, cmd):
        conn = sqlite3.connect(self.mexm_sqlite_path)
        conn.execute(cmd)
        conn.commit()
        conn.close()

    def create_job_table(self):
        if self.check_if_table_exists(table_name='simulation_jobs'):
            cmd = 'DROP TABLE simulation_jobs;'
            self.execute_command(cmd)
        else:
            cmd = (
                'CREATE TABLE simulation_jobs '
                '('
                '    id int primary key not null,'
                '    path text not null,'
                '    cluster_job_id int,'
                '    cluster_submit_time,'
                '    cluster_status,'
                ');'
            )

    def create_new_simulation_job(self, job_id, job_name, job_path):
        cmd_fmt = (
            "insert into simulation_jobs(job_id, job_name, job_path)"
            "values ({job_id}, '{job_name}', '{job_path}');"
        )
        cmd = cmd_fmt.format(job_id=job_id, job_name=job_name, job_path=job_path)
        print(cmd)
        #self.execute_command(cmd)

    def check_if_table_exists(self, table_name):
        conn = sqlite3.connect(self.mexm_sqlite_path)
        cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        cursor = conn.execute(cmd.format(table_name=table_name))

        if len(cursor.fetchall()) == 0:
            return False
        else:
            return True
        print(len(cursor.fetchall()))
        

mexm_sqlite_path = 'mexm.db'
sql_conn = sqlite3.connect('test.db')
print('opened database')

if False:
    sql_cmd = '''create table company
        (id int primary key not null,
        name text not null,
        age int not null,
        address char(50),
        salary real);'''
    sql_conn.execute(sql_cmd)
    print('created table')
    sql_conn.close()

if False:
    sql_conn.execute("insert into company(id, name, age, address, salary) \
        values (1, 'Paul', 32, 'California', 20000.00)")
    sql_conn.commit()

sql_conn.execute('update company set salary = 25000.00 where ID = 1 ')
cursor = sql_conn.execute("select id, name, address, salary from company")
for row in cursor:
    print(row)

if __name__ == "__main__":
    o = JobOverlordDatabase()
    o.create_new_simulation_job(job_id=1, job_name='name', job_path='path')