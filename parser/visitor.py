#####################################################################
#                                                                   #
# File auto-generated with `generate_ast.py`. Do not edit directly. #
#                                                                   #
#####################################################################

from abc import ABC, abstractmethod

from expr import *


class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: Binary):
        raise NotImplementedError

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping):
        raise NotImplementedError

    @abstractmethod
    def visit_boolliteral_expr(self, expr: BoolLiteral):
        raise NotImplementedError

    @abstractmethod
    def visit_numliteral_expr(self, expr: NumLiteral):
        raise NotImplementedError

    @abstractmethod
    def visit_stringliteral_expr(self, expr: StringLiteral):
        raise NotImplementedError

    @abstractmethod
    def visit_unary_expr(self, expr: Unary):
        raise NotImplementedError
