"""Entry point for the Jipy Language."""
import sys
from os import path

from jipy.scanner import Scanner
from jipy.parser import Parser
from jipy.error import JipyError
from jipy.token_types import TokenTypes
from jipy.ast_printer import AstPrinter
from jipy.interpreter import Interpreter


class Jipy:
    def __init__(self):
        self.HAD_ERROR = False
        self.interpreter = Interpreter()

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
            if JipyError.HAD_ERROR:
                sys.exit()

    def run_prompt(self):
        """Run jipy in REPL."""
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            except KeyboardInterrupt:
                print("Keyboard Interrupt")
            else:
                if line:
                    self.run(line)
                    JipyError.HAD_ERROR == False

    def run(self, source):
        """TODO."""
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        if len(tokens) == 1:
            if tokens[0].token_type is TokenTypes.EOF:
                JipyError.error(tokens[0], "Source file is empty")
        parser = Parser(tokens)
        expression = parser.parse()
        if JipyError.HAD_ERROR:
            return
        print(AstPrinter().print(expression))


if __name__ == "__main__":
    jipy_interpretor = Jipy()
    jipy_interpretor.jipy(sys.args[1:])
