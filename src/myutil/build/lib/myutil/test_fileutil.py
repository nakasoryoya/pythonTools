from unittest import TestCase
from src.common.fileutil import output_dictionary_to_file


class Test(TestCase):
    def test_output_dictionary_to_file(self):
        dict = [{'name': 'test', 'age': 20}, {'name': 'test2', 'age': 30}]
        output_file = './output.txt'
        output_dictionary_to_file(dict, output_file)
