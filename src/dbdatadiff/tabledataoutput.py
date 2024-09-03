import sys

import myutil.configReader as configReader
from myutil.dbutil import DatabaseAccessor
from myutil.fileutil import File
from myutil.fileutil import TextFile
from myutil.fileutil import Directory


def main():
    conf = configReader.read_configuration('setting.conf', 'connection')

    database_accessor = DatabaseAccessor(
        conf['driver'], conf['server'], conf['database'], conf['username'], conf['password'])

    target_table = conf['target_table'].split(',')

    out_dir = Directory(File(sys.argv[0]).get_parent().get_path()+"/out")
    if not out_dir.is_exist():
        out_dir.create()

    for table in target_table:
        database_accessor.execute_update_sql(f'use {conf["database"]}')
        table_data = database_accessor.execute_sql(f"select * from {table}")

        text_file = TextFile(f'{out_dir.get_path()}/{table}.txt')
        text_data = ''
        for columns in table_data[0].keys():
            text_data += columns + '\t'

        text_data += '\n'
        for data in table_data:
            for value in data.values():
                text_data += str(value) + '\t'
            text_data += '\n'

        text_file.set_text(text_data)
        text_file.save()


if __name__ == "__main__":
    main()
