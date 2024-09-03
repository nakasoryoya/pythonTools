from unittest import TestCase
import src.common.excelutil as excelutil


class Test(TestCase):
    def test_output_dictionary_to_excel(self):
        dic = [{'name': 'test', 'age': 20}, {'name': 'test2', 'age': 30}]
        output_file = './output.xlsx'
        excelutil.output_dictionary_to_excel(dic, output_file)
