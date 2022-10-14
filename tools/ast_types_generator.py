import os, shutil
from collections import namedtuple
from typing import List, Tuple, Dict

AST_TYPES_DIR: str = os.path.join(os.getcwd(), "modules", "ast_types")
GENERAL_IMPORTS: str = "from abc import ABC\nfrom dataclasses import dataclass\n"

EXPR_FILE: str = os.path.join(AST_TYPES_DIR, "expr_types.py")
EXPR_IMPORTS: str = "from tokenizer.token_types import Token\n"
EXPR_BASE: str = "Expr"
EXPR_DESCRIPTION: Dict[str, str] = {
    "ExprBinary"   : f"{EXPR_BASE} left, Token operator, {EXPR_BASE} right",
    "ExprGrouping" : f"{EXPR_BASE} expression",
    "ExprLiteral"  : "object value",
    "ExprUnary"    : f"Token operator, {EXPR_BASE} right"
}

FILES = (EXPR_FILE, )
IMPORTS = (EXPR_IMPORTS, )
BASES = (EXPR_BASE, )
DESCRIPTIONS = (EXPR_DESCRIPTION, )

assert len(FILES) == len(IMPORTS) == len(BASES) == len(DESCRIPTIONS)


TreeClassType = namedtuple("TreeClassType", ["name", "members"])
TreeClassMemberType = namedtuple("TreeClassMemberType", ["type", "name"])

def parse_description(description: Dict[str, str]) -> List[TreeClassType]:
    def _parse_type(name: str, members_description: str) -> Tuple[str, List[TreeClassMemberType]]:
        members: List = []
        for m in members_description.split(", "):
            member_type, member_name = m.split(" ") 
            members.append(TreeClassMemberType(member_type, member_name))
        
        return name, members

    return [TreeClassType(*_parse_type(name, members_description)) for name, members_description in description.items()]

def generate_code_str(base_class_name: str, tree_class_types: List[TreeClassType], imports: str) -> str:
    base_class: str = f"class {base_class_name}(ABC):\n    pass\n"

    classes: str = "\n".join([
        f"@dataclass\nclass {t.name}({base_class_name}):\n    " + \
            "    ".join([f"{member.name}: {member.type}\n" for member in t.members])
        for t in tree_class_types
    ])

    return "\n".join([GENERAL_IMPORTS, imports, base_class, classes])


if __name__ == "__main__":
    if os.path.isdir(AST_TYPES_DIR):
        shutil.rmtree(AST_TYPES_DIR)
    os.mkdir(AST_TYPES_DIR)

    for file, imports, base, description in zip(FILES, IMPORTS, BASES, DESCRIPTIONS):
        with open(file, "w") as f:
            f.write(generate_code_str(base, parse_description(description), imports))