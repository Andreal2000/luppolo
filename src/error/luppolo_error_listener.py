from antlr4.error.ErrorListener import ErrorListener


def str_yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m"


def str_red(text: str) -> str:
    return f"\033[91m{text}\033[0m"


def str_bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def format_message(title: str, text: str, source_code: str, highlighted: str) -> str:
    return f"""
{title}: {text}
{source_code}
{highlighted}
"""


class LuppoloErrorListener(ErrorListener):
    def __init__(self) -> None:
        super().__init__()
        self.errors = 0
        self.warnings = 0

    def getErrorCount(self):
        return self.errors

    def getWarningCount(self):
        return self.warnings

    def reportAmbiguity(
        self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs
    ):
        return super().reportAmbiguity(
            recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs
        )

    def reportAttemptingFullContext(
        self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs
    ):
        return super().reportAttemptingFullContext(
            recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs
        )

    def reportContextSensitivity(
        self, recognizer, dfa, startIndex, stopIndex, prediction, configs
    ):
        return super().reportContextSensitivity(
            recognizer, dfa, startIndex, stopIndex, prediction, configs
        )

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Retrieve the input list (lines of code) from the recognizer
        input_list = recognizer.getInputStream().tokenSource.inputStream.strdata.split(
            "\n"
        )
        error_line = input_list[line - 1]

        # Check if it's a syntax warning (e.g., automatically recoverable) or an error
        if e is None:
            # Warning case: Automatically recoverable error
            self.warnings += 1

            title = f"{str_yellow('warning')} at line {str_bold(str(line))}, column {str_bold(str(column))}"
            source_code = f"{error_line[:column-1]}{str_yellow(error_line[column-1:column+len(offendingSymbol.text)])}{error_line[column+len(offendingSymbol.text):]}"
            highlighted = str_yellow(" " * (column) + "^" * len(offendingSymbol.text))

            # Format the output and print
            print(format_message(title, msg, source_code, highlighted), end="")

        else:
            # Error case: Non-recoverable syntax error
            self.errors += 1

            title = f"{str_red('error')} at line {str_bold(str(line))}, column {str_bold(str(column))}"
            source_code = f"{error_line[:column-1]}{str_red(error_line[column-1:column+len(offendingSymbol.text)])}{error_line[column+len(offendingSymbol.text):]}"
            highlighted = str_red(" " * (column) + "^" * len(offendingSymbol.text))

            # Format the output and print
            print(format_message(title, msg, source_code, highlighted), end="")
