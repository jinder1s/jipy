#!/usr/bin/env python3
"""Scanner for jipy language."""
from .token_types import TokenTypes


class Scanner:
    def __init__(self, source):
        self.source = source

        self._start = 0
        self._current = 0
        self._line = 1

    def is_end(self):
        return self._current == len(self.source)

    def scan_tokens(self):
        pass
