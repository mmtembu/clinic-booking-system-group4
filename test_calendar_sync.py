import os
import unittest
from unittest.mock import patch
import sys
import json
from test_base import run_unittests
from test_base import captured_io
from io import StringIO
import hashlib
import calendar_sync

class TestMyFunction(unittest.TestCase):
    # def test_fetch_calendar_events(self):
    #     events = "yes"
    #     calendar_sync.fetch_calendar_events(events, "clinix")
    #     self.assertTrue(os.path.exists("clinix.json"))


    def test_is_calendar_current_data_old(self):
        events = "yes"
        self.assertTrue(calendar_sync.is_calendar_current_data_old(events, "student"))
        self.assertFalse(calendar_sync.is_calendar_current_data_old(events, "student"))

    
    def test_from_csv_to_dict(self):
        pass