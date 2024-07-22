import sys


def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    sys.stderr.write(f"[line {line}] Error{where}: {message}\n")
