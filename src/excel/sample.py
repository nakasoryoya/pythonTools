import src.common.excelutil as excelutil


def main():
    result = excelutil.input_range_into_list('sample.xlsx', 'Sheet', 1, 6, 1, 4)
    for row in result:
        print(row)


if __name__ == "__main__":
    main()
