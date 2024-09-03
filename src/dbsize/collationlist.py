from src.common.excelutil import WorkBook
from src.common.dbutil import DatabaseAccessor

wb = WorkBook('collation.xlsx')
li = wb.get_worksheet('Sheet').input_range_into_list(1, 42, 1, 1)

clname_list = []
for db in li:
    da = DatabaseAccessor('ODBC Driver 18 for SQL Server', '172.23.144.224', db[0], 'imart', 'admin')
    da.execute_sql("use " + db[0])
    clname = (da.execute_sql("select name, collation_name from sys.databases"))
    clname_list.append(clname[0])

ws = wb.create_worksheet('Sheet2')
ws.output_dictionary_to_excel(clname_list, 1, 1)
wb.save()

