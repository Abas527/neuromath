from .tokens import Token
from .token_types import TokenType

class Lexer():
    def __init__(self,text:str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.line = 1
        self.column = 1
    
    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def peek(self):
        if self.pos + 1 < len(self.text):
            return self.text[self.pos + 1]
        else:
            return None
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def number(self):
        result=""
        line=self.line
        column=self.column
        dot_count=0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char=='.'):
            
            if self.current_char=='.':
                dot_count+=1
                if dot_count > 1:
                    raise Exception(f"Invalid number format at line {line} column {column}")
            result+=self.current_char
            self.advance()

        if "." in result:
            return Token(TokenType.NUMBER, float(result), line, column)
            
        return Token(TokenType.NUMBER, int(result), line, column)
    def identifier(self):
        result=""
        line=self.line
        column=self.column

        while self.current_char and (self.current_char.isalnum() or self.current_char=='_'):
            result+=self.current_char
            self.advance()
        
        return Token(TokenType.IDENTIFIER, result, line, column)
    
    
    def get_next_token(self):
        while self.current_char:

            #skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            #skip comments
            if self.current_char=='#':
                self.skip_comment()
                continue

            # newline
            if self.current_char=='\n':
                token=Token(TokenType.NEWLINE, line=self.line, column=self.column)
                self.advance()
                return token

            #identifiers
            if self.current_char.isalpha() or self.current_char=='_':
                return self.identifier()
            
            #numbers
            if self.current_char.isdigit() or (self.current_char=='.' and self.peek() and self.peek().isdigit()):
                return self.number()
            
            #operators
            if self.current_char=='+':
                token=Token(TokenType.PLUS, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char=='-':
                token=Token(TokenType.MINUS, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char=='*' and self.peek()=='*':
                token=Token(TokenType.POW, line=self.line, column=self.column)
                self.advance()
                self.advance()
                return token
            
            if self.current_char=="%" :
                token=Token(TokenType.MOD, line=self.line, column=self.column)
                self.advance()
                return token 

            if self.current_char=='*':
                token=Token(TokenType.MUL, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char=='/':
                token=Token(TokenType.DIV, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char=='^':
                token=Token(TokenType.POW, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char=='=':
                token=Token(TokenType.ASSIGN, line=self.line, column=self.column)
                self.advance()
                return token
            
            #delimiters
            if self.current_char=='(':
                token=Token(TokenType.LPAREN, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char==')':
                token=Token(TokenType.RPAREN, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char==',':
                token=Token(TokenType.COMMA, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char=='[':
                token=Token(TokenType.LBRACKET, line=self.line, column=self.column)
                self.advance()
                return token
            if self.current_char==']':
                token=Token(TokenType.RBRACKET, line=self.line, column=self.column)
                self.advance()
                return token
            
            raise Exception(f"Unknown character '{self.current_char}' at line {self.line}, {self.column}")
        return Token(TokenType.EOF, line=self.line, column=self.column)
    
    def tokenize(self):
        tokens=[]
        while True:
            token=self.get_next_token()
            tokens.append(token)
            if token.type==TokenType.EOF:
                break
        return tokens
