import os
import re
import sqlite3

from backend.settings import BASE_DIR

db_sqlite3 = os.path.join(BASE_DIR, "db.sqlite3")


def get_replace_string(string):
    """
    替换字符串
    """

    pattern = re.compile(r'\${' + r'\w+' + r'}', re.M | re.S)
    replace_list = re.findall(pattern, str(string))
    if replace_list:
        for r in replace_list:
            name = r.split('{')[1][:-1]
            conn = sqlite3.connect(db_sqlite3)
            cursor = conn.cursor()
            sql = f"select value from cases_testextract where name='{name}'"
            extract_obj = cursor.execute(sql).fetchone()
            conn.close()
            string = re.sub(pattern, extract_obj[0], str(string))
            return string
    else:
        return string


def update_extract(value, case_id, name):
    """
    更新 extract 数据
    """

    conn = sqlite3.connect(db_sqlite3)
    cursor = conn.cursor()
    sql = f"update cases_testextract set value='{value}' where case_id='{case_id}' and name='{name}'"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def select_extract(case_id):
    """
    查询 extract 数据
    """

    conn = sqlite3.connect(db_sqlite3)
    cursor = conn.cursor()
    sql = f"select name, extract from cases_testextract where case_id='{case_id}'"
    extract_obj = cursor.execute(sql).fetchall()
    conn.close()
    return extract_obj
