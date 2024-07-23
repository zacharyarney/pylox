from io import TextIOWrapper
import sys
from typing import Text


def generate_ast():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python generate_ast <output directory>")
        sys.exit(64)
    output_dir = sys.argv[1]
    _define_visitor(output_dir)
    _define_ast(
        output_dir,
        "Expr",
        [
            "Binary        | left: Expr, operator: Token, right: Expr",
            "Grouping      | expression: Expr",
            "BoolLiteral   | value: bool",
            "NumLiteral    | value: float",
            "StringLiteral | value: str",
            "Unary         | operator: Token, right: Expr",
        ],
    )


def _add_comment(file: TextIOWrapper):
    file.write(
        "#####################################################################\n"
    )
    file.write(
        "#                                                                   #\n"
    )
    file.write(
        "# File auto-generated with `generate_ast.py`. Do not edit directly. #\n"
    )
    file.write(
        "#                                                                   #\n"
    )
    file.write(
        "#####################################################################\n"
    )
    file.write("\n")


def _define_ast(output_dir: str, base_name: str, types: list[str]):
    path = output_dir + "/" + base_name.lower() + ".py"
    visitor_path = output_dir + "/visitor.py"
    try:
        with open(path, "w") as file:
            _add_comment(file)
            # imports
            file.write("from abc import ABC\n")
            file.write("from dataclasses import dataclass\n")
            file.write("\n")
            file.write("from lexer import Token\n")
            file.write("\n\n")
            # base class
            file.write(f"class {base_name}(ABC):\n")
            file.write("    pass\n")
            file.write("\n\n")
            # AST classes
            for type in types:
                node_info = type.split("|")
                class_name = node_info[0].rstrip()
                fields = node_info[1].lstrip().split(",")
                _define_type(file, base_name, class_name, fields)
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(66)
    try:
        with open(visitor_path, "r+") as visitor_file:
            for type in types:
                lines = visitor_file.readlines()
                last_line = lines[-1]
                if last_line != "class Visitor(ABC):\n":
                    visitor_file.write("\n")
                node_info = type.split("|")
                class_name = node_info[0].rstrip()
                _define_visitor_types(visitor_file, base_name, class_name)
                # visitor_file.flush()
                visitor_file.seek(0)

    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(66)


def _define_type(
    file: TextIOWrapper, base_name: str, class_name: str, fields: list[str]
):
    file.write("@dataclass\n")
    file.write(f"class {class_name}({base_name}):\n")
    for field in fields:
        file.write(f"    {field.lstrip()}\n")
    file.write("\n\n")


def _define_visitor(output_dir: str):
    path = output_dir + "/visitor.py"
    try:
        with open(path, "w") as file:
            _add_comment(file)
            # imports
            file.write("from abc import ABC, abstractmethod\n")
            file.write("\n")
            file.write("from expr import *\n")
            file.write("\n\n")
            file.write("class Visitor(ABC):\n")
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(66)


def _define_visitor_types(file: TextIOWrapper, base_name: str, class_name: str):
    file.write("    @abstractmethod\n")
    file.write(
        f"    def visit_{class_name.lower()}_{base_name.lower()}(self, {base_name.lower()}: {class_name}):\n"
    )
    file.write("        raise NotImplementedError\n")


if __name__ == "__main__":
    generate_ast()
