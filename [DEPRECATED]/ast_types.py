from dataclasses import dataclass
from abc import ABC
from token_classes import Token

EXPR_BASE_NAME = "_Expr"

EXPR_CLASSE_DESCRIPTION = {
    "ExprBinary"   : "Expr left, Token operator, Expr right",
    "ExprGrouping" : "Expr expression",
    "ExprLiteral"  : "Object value",
    "ExprUnary"    : "Token operator, Expr right"
}

