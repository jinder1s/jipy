"""Entry point for the Jipy Language."""
import sys
from os import path

from .scanner import Scanner


HAD_ERROR = False


def jipy(args: list = None):
    """Entry point for the jipy language."""
    if len(args) > 1:
        raise Exception("You passed in too many values to Jipy")
    if len(args) == 1 and path.isfile(args[0]):
        run_file(args[0])
    else:
        run_prompt()


def run_file(source_file_path):
    """TODO."""
    with open(source_file_path) as source_file:
        source = source_file.readlines()
        run(source)
        global HAD_ERROR
        if HAD_ERROR:
            sys.exit()


def run_prompt():
    """Run jipy in REPL."""
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        else:
            if line:
                run(line)
                global HAD_ERROR
                HAD_ERROR = False


def run(source):
    """TODO."""
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(token)


def error(line_num, message):
    """TODO."""
    report(line_num, "", message)


def report(line_num, where, message):
    """UI for error reporting."""
    print(f"[line {line_num}] Error {where}: {message}")
    global HAD_ERROR
    HAD_ERROR = True


if __name__ == "__main__":
    jipy(sys.args[1:])
