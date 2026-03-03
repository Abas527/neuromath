from .lexer import Lexer
from .token_types import TokenType
from .tokens import Token


code="""
x = 3 + 4.4 * (2 - 1) ** 2%5"""

lexer=Lexer(code)
tokens=lexer.tokenize()
for token in tokens:
    print(token)