from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()

    # operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    # alias for backwards compatibility
    MUL = MULTIPLY
    DIV = auto()
    POW = auto()
    MOD = auto()

    ASSIGN = auto()

    # delimiters
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()

    # identifier subtypes returned by lexer
    VARIABLE = auto()
    FUNCTION = auto()

    EOF = auto()
    NEWLINE = auto()
