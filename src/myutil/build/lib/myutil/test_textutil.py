from unittest import TestCase
import myutil.textutil as textutil


class Test(TestCase):
    def test_base64_encode(self):
        print(textutil.base64_encode('test'.encode('utf-8')))
        print(textutil.base64_decode('dGVzdA=='))

    def test_url_decode(self):
        print(textutil.url_decode('http://172.23.144.222/redmines/dept/projects/dept-infra-req/wiki/%E9%83%A8%E5%86'
                                  '%85%E3%82%A4%E3%83%B3%E3%83%95%E3%83%A9%E7%AA%93%E5%8F%A3%E3%81%AE%E3%81%94%E6%A1'
                                  '%88%E5%86%85'))

        print(textutil.url_encode(
            'http://172.23.144.222/redmines/dept/projects/dept-infra-req/wiki/部内インフラ窓口のご案内'))
