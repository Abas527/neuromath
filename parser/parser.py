from neuromath.lexer.lexer import Lexer
from neuromath.lexer.token_types import TokenType
from neuromath.parser.ast_nodes import *

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Expected token {token_type} but got {self.current_token}")
    
    def parse(self):
        statements = []
        while self.current_token and self.current_token.type != TokenType.EOF:
           
            statements.append(self.statement())
        return Program(statements)
    
    def statement(self):
        if (self.current_token.type == TokenType.IDENTIFIER and self.peek() and self.peek().type == TokenType.LPAREN):

            old_pos = self.pos
            self.advance()  
            next_after_paran = self.peek_next_after_rparen()
            self.pos = old_pos
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None


            if next_after_paran and next_after_paran.type == TokenType.ASSIGN:
                return self.function_definition()
     
        # Assignment
        if self.current_token.type == TokenType.IDENTIFIER and self.peek() and self.peek().type == TokenType.ASSIGN:
            return self.assignment()
    
        return self.expr()
    
    def peek_next_after_rparen(self):

        if self.current_token.type != TokenType.LPAREN:
            raise Exception(f"Expected LPAREN but got {self.current_token}")
        
        depth=1
        
        i = self.pos + 1
        depth = 1  # because we already saw LPAREN
        while i < len(self.tokens):
            if self.tokens[i].type == TokenType.LPAREN:
                depth += 1
            elif self.tokens[i].type == TokenType.RPAREN:
                depth -= 1
                if depth == 0:
                    return self.tokens[i + 1] if i + 1 < len(self.tokens) else None
            i += 1
        return None
    def assignment(self):
        identifier = Identifier(self.current_token.value)
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        value = self.expr()
        return Assignment(identifier, value)
    
    def expr(self):
        node = self.term()
        while self.current_token and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.type
            self.advance()
            node = BinaryOp(node, op, self.term())
        return node
    
    def term(self):
        node=self.power()
        while self.current_token and self.current_token.type in (TokenType.MUL, TokenType.DIV, TokenType.MOD):
            op=self.current_token.type
            self.advance()
            node=BinaryOp(node,op,self.power())
        return node
    
    def power(self):
        node=self.factor()
        if self.current_token and self.current_token.type==TokenType.POW:
            op=self.current_token.type
            self.advance()
            node=BinaryOp(node,op,self.power())
        return node
    def factor(self):
        token=self.current_token
        if token.type in (TokenType.PLUS, TokenType.MINUS):
            self.advance()
            return UnaryOp(token.type, self.factor())
        return self.primary()
    
    def primary(self):
        token=self.current_token
        if token.type==TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        if token.type==TokenType.IDENTIFIER:
            if self.peek() and self.peek().type==TokenType.LPAREN:
                return self.function_call()
            self.advance()
            return Identifier(token.value)
        
        if token.type==TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node=self.expr()
            self.eat(TokenType.RPAREN)
            return node
        if token.type==TokenType.LBRACKET:
            return self.matrix()
        
        raise Exception(f"Unexpected token {token.type} at line {token.line}, column {token.column}")

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None
    
    def function_call(self):
        name=self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        args=[]
        
        while self.current_token and self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.LBRACKET:
                args.append(self.vector_or_matrix())
            else:
                args.append(self.expr())
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        self.eat(TokenType.RPAREN)
        return FunctionCall(name, args)
    
    def function_definition(self):
        name=self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        params=[]
        if self.current_token.type!=TokenType.RPAREN:
            params.append(Identifier(self.current_token.value))
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type==TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(Identifier(self.current_token.value))
                self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.ASSIGN)
        body=self.expr()
        return FunctionDef(name,params,body)
    
    def vector_or_matrix(self):
        self.eat(TokenType.LBRACKET)

        if self.current_token.type == TokenType.LBRACKET:

            # matrix
            rows=[self.row()]
            while self.current_token and self.current_token.type==TokenType.COMMA:
                self.eat(TokenType.COMMA)
                rows.append(self.row())
            self.eat(TokenType.RBRACKET)
            return Matrix(rows)

        # vector
        elements=[]
        elements.append(self.expr())
        while self.current_token and self.current_token.type==TokenType.COMMA:
            self.eat(TokenType.COMMA)
            elements.append(self.expr())
        self.eat(TokenType.RBRACKET)
        return Vector(elements)        
    
    def matrix(self):
        return self.vector_or_matrix()
    
    def row(self):
        elements=[]
        self.eat(TokenType.LBRACKET)
        elements.append(self.expr())
        while self.current_token.type==TokenType.COMMA:
            self.eat(TokenType.COMMA)
            elements.append(self.expr())
        self.eat(TokenType.RBRACKET)
        return elements
