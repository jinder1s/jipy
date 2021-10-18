"""Entry point for the Jipy Language."""
import sys
from os import path

from jipy.scanner import Scanner


class Jipy:
    def __init__(self):
        self.HAD_ERROR = False

    def jipy(self, args: list = None):
        """Entry point for the jipy language."""
        if len(args) > 1:
            raise Exception("You passed in too many values to Jipy")
        if len(args) == 1 and path.isfile(args[0]):
            self.run_file(args[0])
        else:
            self.run_prompt()

    def run_file(self, source_file_path):
        """TODO."""
        with open(source_file_path) as source_file:
            source = source_file.read()
            self.run(source)
            if self.HAD_ERROR:
                sys.exit()

    def run_prompt(self):
        """Run jipy in REPL."""
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            else:
                if line:
                    self.run(line)
                    self.HAD_ERROR = False

    def run(self, source):
        """TODO."""
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    def error(self, line_num, message):
        """TODO."""
        self.report(line_num, "", message)

    def report(self, line_num, where, message):
        """UI for error reporting."""
        print(f"[line {line_num}] Error {where}: {message}")
        self.HAD_ERROR = True


if __name__ == "__main__":
    jipy_interpretor = Jipy()
    jipy_interpretor.jipy(sys.args[1:])
