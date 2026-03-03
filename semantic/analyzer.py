from neuromath.parser.parser import Parser
from neuromath.parser.ast_nodes import *
from neuromath.semantic.symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def analyze(self,node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_analyze)
        return method(node)
    
    def generic_analyze(self,node):
        raise Exception(f"No visit_{type(node).__name__} method defined")
    
    def visit_Program(self,node):
        for stmt in node.statements:
            self.analyze(stmt)
    
    def visit_Assignment(self,node):
        var_name = node.identifier.name
        self.analyze(node.value)
        self.symbol_table.define_variable(var_name)
    
    def visit_Number(self,node):
        pass

    def visit_Identifier(self,node):
        var_name = node.name
        if not self.symbol_table.is_variable_defined(var_name):
            raise Exception(f"Undefined variable '{var_name}'")
    
    def visit_UnaryOp(self,node):
        self.analyze(node.operand)

    def visit_BinaryOp(self,node):
        self.analyze(node.left)
        self.analyze(node.right)
    
    def visit_FunctionCall(self,node):
        
        if not self.symbol_table.is_function_defined(node.name):
            raise Exception(f"Undefined function '{node.name}' at line {node.line} column {node.column}")
        
        expected_arity = self.symbol_table.function_arity(node.name)

        if len(node.arguments) != expected_arity:
            raise Exception(f"Function '{node.name}' expects {expected_arity} arguments but got {len(node.arguments)} at line {node.line} column {node.column}")
        
        for arg in node.arguments:
            self.analyze(arg)
    
    def visit_Matrix(self,node):

        if len(node.rows) == 0:
            raise Exception(f"Matrix cannot be empty at line {node.line} column {node.column}")
        
        row_length = len(node.rows[0])


        for row in node.rows:
            if len(row) != row_length:
                raise Exception(f"All rows in a matrix must have the same number of elements at line {node.line} column {node.column}")
            for element in row:
                self.analyze(element)