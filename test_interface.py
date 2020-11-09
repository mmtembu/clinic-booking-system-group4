import os
import unittest
from unittest.mock import patch
from io import StringIO
from interface import create_profile

class MyTestFunction(unittest.TestCase):
    @patch("sys.stdin", StringIO("tsithole\nJHB\n"))
    def test_create_profile(self):
        self.assertEqual(create_profile(),"""Profile Created""")


if __name__ == '__main__':
    unittest.main()