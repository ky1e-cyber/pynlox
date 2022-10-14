from abc import ABC
from dataclasses import dataclass

from tokenizer.token_types import Token

class Expr(ABC):
    pass

@dataclass
class ExprBinary(Expr):
    left: Expr
    operator: Token
    right: Expr

@dataclass
class ExprGrouping(Expr):
    expression: Expr

@dataclass
class ExprLiteral(Expr):
    value: object

@dataclass
class ExprUnary(Expr):
    operator: Token
    right: Expr
