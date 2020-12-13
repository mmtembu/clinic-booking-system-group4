import os
import unittest
from unittest.mock import patch
import sys
import json
from test_base import run_unittests
from test_base import captured_io
from io import StringIO
import hashlib
import create_volunteer_slot

class MyTestFunction(unittest.TestCase):
    def test_time_start(time, mins):
        self.assertEqual(create_volunteer_slot.time_start())
