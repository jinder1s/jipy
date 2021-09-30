#!/usr/bin/env python3

import pytest
from unittest import TestCase
from jipy.scanner import Scanner

class TestScanner(TestCase):

    def setUp(self):

        source = """blah \n
hehe"""
        self.scanner = Scanner(source)
