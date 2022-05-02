import unittest
from XTestRunner import XMLTestRunner
from ddt import ddt, data, unpack


@ddt
class MyTest(unittest.TestCase):

    @data(
        [1, 2, 2],
        [1, 1, 2])
    @unpack
    def test_api1(self, a, b, c):
        self.assertEqual(a + b, c)


if __name__ == "__main__":
    report = "./xml_test_01.xml"
    with open(report, 'wb') as fp:
        unittest.main(testRunner=XMLTestRunner(output=fp))

