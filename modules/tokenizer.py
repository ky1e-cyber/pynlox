import re
from typing import Tuple, Dict
from modules.classes.tokens import TokenType, Token


def Tokenizer(source_code: str):
    source_code: Tuple[str, ...] = tuple(source_code.splitlines())

    re_whitespace = re.compile(r"\s")

    single_char_map: Dict[str, TokenType()] = {
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        "{": TokenType.LEFT_BRACE,
        "}": TokenType.RIGHT_BRACE,
        ",": TokenType.COMMA,
        ".": TokenType.DOT,
        "-": TokenType.MINUS,
        "+": TokenType.PLUS,
        ";": TokenType.SEMICOLON,
        "*": TokenType.STAR
        }

    double_chars_map: Dict[str, Tuple[str, TokenType, TokenType]] = {
        "=": ("=", TokenType.EQUAL, TokenType.EQUAL_EQUAL),
        "!": ("=", TokenType.BANG, TokenType.BANG_EQUAL),
        ">": ("=", TokenType.GREATER, TokenType.GREATER_EQUAL),
        "<": ("=", TokenType.LESS, TokenType.LESS_EQUAL)
    }

    keywords_map: Dict[str, TokenType] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE 
    }

    def _is_alpha(char: str) -> bool:
        assert len(char) == 1, "string with len != 1 in  _is_alpha, one char expected"
        return ord(char) in range(ord('a'), ord('z') + 1) or ord(char) in range(ord('A'), ord('Z') + 1) or char == '_'

    def _is_alphanumeric(char: str) -> bool:
        assert len(char) == 1, "string with len != 1 in  _is_alphanumeric, one char expected"
        return _is_alpha(char) or char.isdigit()

    def _match_start(segment: str, expected: str) -> bool:
        return segment.startswith(expected)

    def _match_string(segment: str, terminating_char: str) -> int:
        return segment.find(terminating_char)

    def _match_multiline_string(segment: Tuple[str, ...], start: int) -> Tuple[int, int]:
        pos: int = segment[0].find("'''", start)
        if pos != -1:
            return 0, pos
        for line_number, line in enumerate(segment[1::], start = 1):
            pos = line.find("'''")
            if pos != -1:
                return line_number, pos

        return -1, -1

    def _get_multiline_string(segment: Tuple[str, ...], start_pos: int,  end_pos: int) -> str:
        if len(segment) == 1:
            return segment[0][start_pos:end_pos:]

        return "\n".join((segment[0][start_pos::], ) + segment[1:-1:] + (segment[-1][:end_pos:], ))

    def _match_number(segment: str) -> int:
        for pos, char in enumerate(segment):
            if char.isdigit():
                continue

            if char == '.':
                if (pos < len(segment) - 1) and segment[pos + 1].isdigit():
                    continue
            
            return pos 
        return len(segment)


    def _match_identifier(segment: str) -> int:
        for pos, char in enumerate(segment):
            if _is_alphanumeric(char):
                continue
            return pos

        return len(segment)


    line_number: int = 0
    line_start: int = 0

    while line_number < len(source_code):
        ls: int = line_start 
        line_start = 0
        for pos, char in enumerate(source_code[line_number][ls::], start = ls):
            if re.match(re_whitespace, char):
                continue

            if char in single_char_map.keys():
                yield Token(single_char_map[char], (line_number + 1, pos))
                continue

            if char in double_chars_map.keys():
                expected, type_unmatch, type_match = double_chars_map[char]

                if _match_start(source_code[line_number][pos + 1::], expected):
                    yield Token(type_match, (line_number + 1, pos))

                    line_start = pos + len(expected) + 1
                    line_number -= 1
                    break
                else:
                    yield Token(type_unmatch, (line_number + 1, pos))
                    continue
            
            if char in {"'", '"'}:
                if _match_start(source_code[line_number][pos::], "'''"):
                    end_line_offset, end_pos = _match_multiline_string(source_code[line_number::], pos + 3)

                    if end_line_offset == -1:
                        yield Token(TokenType.UNEXPECTED, (line_number + 1, pos))
                        return

                    yield Token(
                        TokenType.STRING, 
                        (line_number + 1, pos),
                        literal = _get_multiline_string(
                            source_code[line_number:line_number + end_line_offset + 1:],
                            pos + 3, 
                            end_pos
                            )
                        ) 
                    
                    line_start = end_pos + 3
                    line_number = line_number + end_line_offset - 1

                else:
                    end_pos = _match_string(source_code[line_number][pos + 1::], char)

                    if end_pos == -1:
                        yield Token(TokenType.UNEXPECTED, (line_number + 1, pos))
                        break

                    yield Token(TokenType.STRING, (line_number + 1, pos), literal = source_code[line_number][pos + 1:end_pos:])

                    line_start = end_pos + 1
                    line_number -= 1


            if char.isdigit():
                end_pos = pos + _match_number(source_code[line_number][pos + 1::])

                yield Token(
                    TokenType.NUMBER, 
                    (line_number + 1, pos), 
                    literal = float(source_code[line_number][pos:end_pos + 1])
                )

                line_start = end_pos + 1
                line_number -= 1

                break
            
            if _is_alpha(char):
                end_pos = pos + _match_identifier(source_code[line_number][pos + 1::])
                name: str = source_code[line_number][pos:end_pos + 1:]
                token_type: TokenType = keywords_map.get(name, TokenType.IDENTIFIER)

                if token_type == TokenType.IDENTIFIER:
                    yield Token(token_type, (line_number + 1, pos), name = name)
                else:
                    yield Token(token_type, (line_number + 1, pos))

                line_start = end_pos + 1
                line_number -= 1

                break

            yield Token(TokenType.UNEXPECTED, (line_number + 1, pos))

        line_number += 1