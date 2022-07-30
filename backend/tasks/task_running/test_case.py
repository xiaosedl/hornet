import json
import os
import sys
from pathlib import Path
import unittest

import jmespath
import requests
from ddt import ddt, file_data
from XTestRunner import XMLTestRunner

BASIC_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASIC_DIR))

from cases.apis.common import get_replace_string, update_extract, select_extract

TEST_DATA = os.path.join(BASIC_DIR, "tasks", "task_running", "test_data.json")
TEST_REPORT = os.path.join(BASIC_DIR, "tasks", "task_running", "xml_test_report.xml")


@ddt
class TaskTest(unittest.TestCase):

    @file_data(TEST_DATA)
    def test_case_api(self, case_id,  url, method, header, params_type, params_body, assert_type, assert_body):

        resp = ""
        url = get_replace_string(url)
        headers = {key: get_replace_string(value) for key, value in header.items()}
        body = {key: get_replace_string(value) for key, value in params_body.items()}

        # 执行用例
        if method == "GET" and params_type.title() == "Params":
            resp = requests.request(method=method, url=url, headers=headers, params=body)
        elif method in ["POST", "PUT", "DELETE"] and params_type.title() == "Form":
            resp = requests.request(method=method, url=url, headers=headers, data=body)
        elif method in ["POST", "PUT", "DELETE"] and params_type.title() == "Json":
            resp = requests.request(method=method, url=url, headers=headers, json=body)

        if assert_type == "include":
            self.assertIn(assert_body, resp.text)
        elif assert_type == "equal":
            self.assertEqual(assert_body, resp.text)

        # 提取变量
        resp_json = json.loads(resp.text)
        extracts = select_extract(case_id)
        if len(extracts) > 0:
            for extract in extracts:
                result = jmespath.search(extract[1], resp_json)
                if result is None:
                    raise ValueError(f"提取器错误：{extract[1]}")
                else:
                    update_extract(value=result, case_id=case_id, name=extract[0])


if __name__ == "__main__":
    with open(TEST_REPORT, 'wb') as fp:
        unittest.main(testRunner=XMLTestRunner(output=fp))
