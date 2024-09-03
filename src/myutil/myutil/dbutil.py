import pyodbc


def cursor_to_dic_list(sql_cursor):
    columns = [column[0] for column in sql_cursor.description]
    rows = sql_cursor.fetchall()
    return [dict(zip(columns, cursor_row)) for cursor_row in rows]


def map_dict_to_obj(org_dict, obj):
    obj_members = obj.__dict__.keys()
    dict_keys = org_dict.keys()
    for key in dict_keys:
        if key in obj_members:
            setattr(obj, key, org_dict[key])
    return obj


class DatabaseAccessor:
    driver = ''
    server = ''
    database = ''
    username = ''
    password = ''
    connection = None

    def __init__(self, driver, server, database, username, password):
        connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};ENCRYPT=no;TRUSTSERVERCERTIFICATE=no'
        self.connection = pyodbc.connect(connectionString)

    def execute_sql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor

    def execute_update_sql(self, sql):
        self.connection.cursor().execute(sql)
        return

    def get_dict_list_by_select_query(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            dict_list = cursor_to_dic_list(cursor)
        return dict_list

    def map_select_query_result_to_obj(self, sql, obj):
        dict_list = self.get_dict_list_by_select_query(sql)
        obj_list = []
        for item in dict_list:
            obj_list.append(map_dict_to_obj(item, obj))
        return obj_list

    def __del__(self):
        self.connection.close()
