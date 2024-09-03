import pyodbc
import src.common.dbutil as dbutil

DRIVER = 'ODBC Driver 18 for SQL Server'
SERVER = '172.23.144.224'
DATABASE = 'master'
USERNAME = 'imart'
PASSWORD = 'admin'

connection = dbutil.get_connection(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD)
result = dbutil.execute_sql(connection, "SELECT name FROM sys.databases")

for db in result:
    try:
        dbutil.execute_sql(connection, "DBCC SHRINKDATABASE (" + db['name'] + ", 10)")
        with open('./shrink.log', 'a') as f:
            f.write(db['name'] + ' shrinked\n')
    except Exception as e:
        with open('./shrink.log', 'a') as f:
            f.write(db['name'] + ' failed\n')
        continue
