import os, shutil
from collections import namedtuple
from typing import List, Tuple, Dict

FILE_PATH = os.path.join(os.getcwd(), "modules", "types", "ast.py")

IMPORTS: str = "from abc import ABC\nfrom dataclasses import dataclass\nfrom tokens import Token\n\n"

EXPR_BASE: str = "Expr"
EXPR_DESCRIPTION: Dict[str, str] = {
    "ExprBinary"   : f"{EXPR_BASE} left, Token operator, {EXPR_BASE} right",
    "ExprGrouping" : f"{EXPR_BASE} expression",
    "ExprLiteral"  : "object value",
    "ExprUnary"    : f"Token operator, {EXPR_BASE} right"
}

BASES = (EXPR_BASE, )
DESCRIPTIONS = (EXPR_DESCRIPTION, )

assert len(BASES) == len(DESCRIPTIONS)


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

def generate_code_str(base_class_name: str, tree_class_types: List[TreeClassType]) -> str:
    base_class: str = f"class {base_class_name}(ABC):\n    pass\n"

    classes: str = "\n".join([
        f"@dataclass\nclass {t.name}({base_class_name}):\n    " + \
            "    ".join([f"{member.name}: {member.type}\n" for member in t.members])
        for t in tree_class_types
    ])

    return "\n".join([base_class, classes])


if __name__ == "__main__":
    if os.path.isfile(FILE_PATH):
        os.remove(FILE_PATH)
    
    with open(FILE_PATH, "w") as f:
        f.write(IMPORTS)
        for base, description in zip(BASES, DESCRIPTIONS):
            f.write(generate_code_str(base, parse_description(description)))
    