class AST():
    """Base class for all AST nodes."""
    pass
class Number(AST):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class Identifier(AST):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Identifier({self.name})"

class BinaryOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op}, {self.right})"

class UnaryOp(AST):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand})"

class Assignment(AST):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value
    def __repr__(self):
        return f"Assignment({self.identifier}, {self.value})"

class Program(AST):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program({self.statements})"

class Matrix(AST):
    def __init__(self, rows):
        self.rows = rows
    def __repr__(self):
        return f"Matrix({self.rows})"
    
class Vector(AST):
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"Vector({self.elements})"

class FunctionCall(AST):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
    def __repr__(self):
        return f"FunctionCall({self.name}, {self.arguments})"
    

class FunctionDef(AST):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body
    def __repr__(self):
        return f"FunctionDef({self.name}, {self.parameters}, {self.body})"