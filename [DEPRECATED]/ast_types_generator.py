from collections import namedtuple
from typing import List, Tuple, Dict
from abc import ABC
from dataclasses import dataclass

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
    base_class: str = f"class {base_class_name}(ABC):\n    pass\n\n"

    classes: str = "\n".join([
        f"@dataclass\nclass {t.name}({base_class_name}):\n    " + \
            "    ".join([f"{member.name}: {member.type}\n" for member in t.members])
        for t in tree_class_types
    ])

    return base_class + classes

def get_namespace(base_name: str, subclasses_description: List[str], namespace: Dict) -> Dict:
    _namespace = namespace.copy()
    _namespace.update({"dataclass": dataclass, "ABC": ABC})

    exec(
        generate_code_str(base_name, parse_description(subclasses_description)),
        _namespace
    )

    return _namespace


### This is the most unnecessary thing that i have ever done