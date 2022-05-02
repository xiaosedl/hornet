import os
from pathlib import Path
import unittest
import requests
from ddt import ddt, file_data
from XTestRunner import XMLTestRunner


BASIC_DIR = Path(__file__).resolve().parent
TEST_DATA = os.path.join(BASIC_DIR, "test_data.json")
TEST_REPORT = os.path.join(BASIC_DIR, "xml_test_report.xml")


@ddt
class TaskTest(unittest.TestCase):

    @file_data(TEST_DATA)
    def test_case_task(self, url, method, header, params_type, params_body, assert_type, assert_body):

        resp = ""
        if method == "GET" and params_type.title() == "Params":
            resp = requests.request(method=method, url=url, headers=header, params=params_body).text
        elif method in ["POST", "PUT", "DELETE"] and params_type.title() == "Form":
            resp = requests.request(method=method, url=url, headers=header, data=params_body).text
        elif method in {"POST", "PUT", "DELETE"} and params_type.title() == "Json":
            resp = requests.request(method=method, url=url, headers=header, json=params_body).text

        if assert_type == "include":
            self.assertIn(assert_body, resp)
        elif assert_type == "equal":
            self.assertEqual(assert_body, resp)


if __name__ == "__main__":
    with open(TEST_REPORT, 'wb') as fp:
        unittest.main(testRunner=XMLTestRunner(output=fp))