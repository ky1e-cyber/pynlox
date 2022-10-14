#!/usr/bin/env python3
import sys
from modules.tokenizer import Tokenizer

def run_script(filename: str):
    with open(filename) as file:
        code_string: str = file.read()

    print(code_string)
    for token in Tokenizer(code_string):
        print(token)

    assert False, "Not implemented"

def run_repl():
    assert False, "Not implemented"
    pass

def main():
    if len(sys.argv) > 2:
        print(f"Usage: {sys.argv[0]} [script]")
        return
    if len(sys.argv) == 2:
        run_script(sys.argv[1])
    else:
        run_repl()

    return

if __name__ == "__main__":
    main()
