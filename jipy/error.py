#!/usr/bin/env python3
#
from jipy.token import Token


class ParserError(Exception):
    def __init__(self, token: Token, error_msg: str):
        # TODO: incorporate token into message
        # TODO: make sure this produces a helpful msg
        self.token = token
        self.message = error_msg
        super().__init__(self.message)

class RunTimeError(Exception):
    def __init__(self, token: Token, error_msg: str):
        # TODO: incorporate token into message
        # TODO: make sure this produces a helpful msg
        self.token = token
        self.message = error_msg
        super().__init__(self.message)

class JipyError:
    log = []
    HAD_ERROR = False
    HAD_RUNTIME_ERROR = False

    @staticmethod
    def report(line_num: int, where: str, message: str):
        """UI for error reporting."""
        log_msg = f"[line {line_num}] Error {where}: {message}"
        print(log_msg)

    @staticmethod
    def error(self, line_num, message):
        """TODO."""
        JipyError.HAD_ERROR = True
        self.report(line_num, "", message)

    @staticmethod
    def run_time_error(self, error: RunTimeError):
        self.HAD_RUNTIME_ERROR = True
        self.report(error.token.line, "", error.message)
