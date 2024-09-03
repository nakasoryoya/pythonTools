from myutil.excelutil import WorkBook


def main():
    wb = WorkBook('C:\\Users\\tie306883\\PycharmProjects\\pythonProject\\src\\excel\\sample.xlsx')
    ws = wb.get_worksheet('Sheet2')
    list = ws.input_range_into_list(1, 9942, 1, 1)
    for row in list:
        fn = str(row[0])
        us = fn.split('_')[0]
        print(len(str(row[0]).split('_')[0]))


def main2():
    wb = WorkBook()
    ws = wb.create_worksheet('Sheet1')
    ws.append(['name', 'age'])
    ws.append(['Alice', 20])
    ws.append(['Bob', 30])

    dic_list = [{'name': 'Alice', 'age': 20}, {'name': 'Bob', 'age': 30}]
    wb.create_worksheet('Sheet2').output_dictionary_to_excel(dic_list, 2, 2)

    wb.save('C:\\Users\\tie306883\\PycharmProjects\\pythonProject\\src\\excel\\sample2.xlsx')


if __name__ == "__main__":
    main()
    #main2()
