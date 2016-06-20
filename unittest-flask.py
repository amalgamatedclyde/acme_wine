__author__ = 'clyde'

import unittest2
import requests

class MyTestCase(unittest2.TestCase):
    url = 'http://127.0.0.1:5000/'

    def test_get(self):
        r = requests.get(self.url)
        self.assertEqual('<Response [200]>', r.__repr__())

    def test_post(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest2.main()
