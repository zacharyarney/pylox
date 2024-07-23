#####################################################################
#                                                                   #
# File auto-generated with `generate_ast.py`. Do not edit directly. #
#                                                                   #
#####################################################################

from abc import ABC
from dataclasses import dataclass

from lexer import Token


class Expr(ABC):
    pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class BoolLiteral(Expr):
    value: bool


@dataclass
class NumLiteral(Expr):
    value: float


@dataclass
class StringLiteral(Expr):
    value: str


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr
