import math
import numpy as np
import sympy as sp
from neuromath.lexer.token_types import TokenType
from neuromath.parser.ast_nodes import *

class Interpreter:
    def __init__(self,variables=None,functions=None):
        self.variables =variables if variables is not None else {
            "pi": math.pi,
            "e": math.e,
        }
        self.sp=sp
        self.np=np
        self.math_functions = {
            "sin":sp.sin,
            "cos":sp.cos,
            "tan":sp.tan,
            "arcsin":sp.asin,
            "arccos":sp.acos,
            "arctan":sp.atan,
            "log":sp.log,
            "ln":sp.log,
            "exp":sp.exp,
            "sqrt":sp.sqrt,
            "abs":sp.Abs,
            "pow":sp.Pow,
        }
        self.functions= functions if functions is not None else {}
        self.builtins={
            "print":self.print_output,
            "typeof":self.typeof,
            "shape":self.matrix_shape,
            "det":self.matrix_determinant,
            "trans":self.matrix_transpose,
            "inv":self.matrix_inverse,
            "identity":self.matrix_identity,
            "zeroes":self.matrix_zeroes,
            "dot":self.dot_product,
            "cross":self.cross_product,
            "norm":self.norm,
            "unit":self.unit_vector,

            # symbolic math functions
            "integrate":self.sym_integrate,
            "diff":self.sym_diff,
            "limit":self.sym_limit,
            "solve":self.sym_solve,
            "summation":self.sym_summation,
            "simplify":self.sym_simplify,
            "factor":self.sym_factor,
            "eigenval":self.np_eigenvalues,
            "solve_linear":self.np_solve_linear,
            "eigenvec":self.np_eigenvectors,

        }
        self.symbolic_functions={"integrate","diff","limit","solve","summation","simplify","factor","eigenval","solve_linear","eigenvec"}
    
    def interpret(self,node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    def generic_visit(self,node):
        raise Exception(f"No visit_{type(node).__name__} method defined")
    
    def typeof(self,value):
        if isinstance(value,list):
            if all(isinstance(elem,(int,float)) for elem in value):
                return "vector"
            elif all(isinstance(elem,list) for elem in value):
                return "matrix"
        return type(value).__name__
    
    def print_output(self,value):
        output_str=str(value)
        print(output_str)
        return output_str
    


    # to_sympy (AST->sympy expression)
    def to_sympy(self,node,symbolic_mode=False):
        if isinstance(node,Identifier):
            if symbolic_mode:
                return sp.Symbol(node.name)
            elif node.name in self.variables:
                return sp.Number(self.variables[node.name])
            return sp.Symbol(node.name)
        elif isinstance(node,Number):
            return sp.Number(node.value)
        elif isinstance(node,BinaryOp):
            left=self.to_sympy(node.left,symbolic_mode)
            right=self.to_sympy(node.right,symbolic_mode)
            if node.op==TokenType.PLUS:
                return left+right
            elif node.op==TokenType.MINUS:
                return left-right
            elif node.op==TokenType.MUL:
                return left*right
            elif node.op==TokenType.DIV:
                return left/right
            elif node.op==TokenType.POW:
                return left**right
            else:
                raise Exception(f"Unknown binary operator '{node.op}'")
        elif isinstance(node,FunctionCall):
            if node.name in self.functions:
                func_def=self.functions[node.name]
                arg_map={
                    p.name: self.to_sympy(a,symbolic_mode) for p, a in zip(func_def.parameters, node.arguments)
                }
                body_expr=self.to_sympy(func_def.body,symbolic_mode=True)
                return body_expr.subs(arg_map)
            elif node.name in self.math_functions:
                args=[self.to_sympy(arg,symbolic_mode) for arg in node.arguments]
                return self.math_functions[node.name](*args)
            elif node.name in self.builtins:
                args=[self.to_sympy(arg,symbolic_mode) for arg in node.arguments]
                return self.builtins[node.name](*args)
            else:
                raise Exception(f"Undefined function '{node.name}'")
        else:
            raise Exception(f"Unknown node type '{type(node).__name__}'")
    
    def visit_Program(self,node:Program):
        result=None
        for statement in node.statements:
            result=self.interpret(statement)
        return result
    
    def visit_Assignment(self,node):
        value=self.interpret(node.value)
        self.variables[node.identifier.name]=value
        print(f"Assigned {node.identifier.name} = {value}")
        return value
    
    def visit_Number(self,node:Number):
        return node.value
    
    def visit_Identifier(self,node):
        if node.name in self.variables:
            return self.variables[node.name]
        else:
            raise Exception(f"Undefined variable '{node.name}'")
        
    def visit_UnaryOp(self,node:UnaryOp):
        operand=self.interpret(node.operand)
        if node.op.type=="PLUS":
            return +operand
        elif node.op.type=="MINUS":
            return -operand
        else:
            raise Exception(f"Unknown unary operator '{node.op.type}'")
    
    def visit_BinaryOp(self,node:BinaryOp):
        left=node.left
        right=node.right

        if isinstance(left,Vector) and isinstance(right,Vector):
            if node.op==TokenType.PLUS:
                return self.vector_add(self.interpret(left),self.interpret(right))
            elif node.op==TokenType.MINUS:
                return self.vector_sub(self.interpret(left),self.interpret(right))
            else:
                raise Exception(f"Unsupported operator '{node.op}' for vectors")
        elif isinstance(left,Matrix) and isinstance(right,Matrix):
            if node.op==TokenType.PLUS:
                return self.matrix_add(self.interpret(left),self.interpret(right))
            elif node.op==TokenType.MINUS:
                return self.matrix_sub(self.interpret(left),self.interpret(right))
            elif node.op==TokenType.MUL:
                return self.matrix_mul(self.interpret(left),self.interpret(right))
            else:
                raise Exception(f"Unsupported operator '{node.op}' for matrices")
        elif (isinstance(right,Matrix) and isinstance(left,(int,float))):
            if node.op==TokenType.MUL:
                return self.matrix_scalar_mul(self.interpret(right),self.interpret(left))
            else:
                raise Exception(f"Unsupported operator '{node.op}' for matrix-scalar multiplication")
        elif (isinstance(right,Vector) and isinstance(left,(int,float))):
            if node.op==TokenType.MUL:
                return [self.interpret(left)*elem for elem in self.interpret(right)]
            else:
                raise Exception(f"Unsupported operator '{node.op}' for vector-scalar multiplication")
        else:
            left=self.interpret(left)
            right=self.interpret(right)

        op=node.op
        if op==TokenType.PLUS:
            return left+right
        elif op==TokenType.MINUS:
            return left-right
        elif op==TokenType.MUL:
            return left*right
        elif op==TokenType.DIV:
            return left/right
        elif op==TokenType.POW:
            return left**right
        elif op==TokenType.MOD:
            return left%right
        else:
            raise Exception(f"Unknown binary operator '{op}'")
        
    def visit_FunctionCall(self, node: FunctionCall):

        # Symbolic functions (diff, integrate)
        if node.name in self.symbolic_functions:
            args = [self.to_sympy(arg,symbolic_mode=True) for arg in node.arguments]
            return self.builtins[node.name](*args)

        #  User-defined functions
        elif node.name in self.functions:
            func_def = self.functions[node.name]
            args = [self.interpret(arg) for arg in node.arguments]
            return self.call_user_function(func_def, args)

        #  Builtins
        elif node.name in self.builtins:
            args = [self.interpret(arg) for arg in node.arguments]
            return self.builtins[node.name](*args)
        elif node.name in self.math_functions:
            args = [self.to_sympy(arg,symbolic_mode=True) for arg in node.arguments]
            return self.math_functions[node.name](*args)

        else:
            raise Exception(f"Undefined function '{node.name}'")
    # def wrap_function(self,node:FunctionDef):
    #     def fnc(*args):
    #         return self.call_user_function(node,args)
    #     return fnc
    
    def call_user_function(self,func,args):
        
        # check arity
        if len(args)!=len(func.parameters):
            raise Exception(f"Expected {len(func.parameters)} arguments but got {len(args)}")
        
        old_variable=self.variables.copy()

        for param, arg in zip(func.parameters, args):
            self.variables[param.name]=arg

        result=self.interpret(func.body)
        self.variables=old_variable
        return result
    
   
    def visit_Matrix(self,node):
        matrix=[]
        for row in node.rows:
            matrix.append([self.interpret(element) for element in row])
        return matrix
    
    def visit_Vector(self,node):
        return [self.interpret(element) for element in node.elements]
    
    def vector_add(self,v1,v2):
        if len(v1)!=len(v2):
            raise Exception("Vectors must have the same length for addition")
        return [v1[i]+v2[i] for i in range(len(v1))]
    
    def vector_sub(self,v1,v2):
        if len(v1)!=len(v2):
            raise Exception("Vectors must have the same length for subtraction")
        return [v1[i]-v2[i] for i in range(len(v1))]
    
    def matrix_add(self,A,B):
        if self.matrix_shape(A)!=self.matrix_shape(B):
            raise Exception("Matrices must have the same shape for addition")
        return [
            [A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A)) ]
    
    def dot_product(self,v1,v2):
        if len(v1)!=len(v2):
            raise Exception("Vectors must have the same length for dot product")
        return sum(v1[i]*v2[i] for i in range(len(v1)))
    
    def cross_product(self,v1,v2):
        if len(v1)!=3 or len(v2)!=3:
            raise Exception("Cross product is only defined for 3D vectors")
        return [
            v1[1]*v2[2]-v1[2]*v2[1],
            v1[2]*v2[0]-v1[0]*v2[2],
            v1[0]*v2[1]-v1[1]*v2[0]
        ]
    def norm(self,v):
        return math.sqrt(sum(elem**2 for elem in v))
    
    def unit_vector(self,v):
        n=self.norm(v)
        if n==0:
            raise Exception("Cannot compute unit vector of zero vector")
        return [elem/n for elem in v]
    def matrix_sub(self,A,B):
        if self.matrix_shape(A)!=self.matrix_shape(B):
            raise Exception("Matrices must have the same shape for subtraction")
        return [
            [A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A)) ]
    
    def matrix_mul(self,A,B):
        if self.matrix_shape(A)[1]!=self.matrix_shape(B)[0]:
            raise Exception("Number of columns in A must equal number of rows in B for multiplication")
        result=[[0 for _ in range(self.matrix_shape(B)[1])] for _ in range(self.matrix_shape(A)[0])]  # Initialize result matrix with zeros
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j]+=A[i][k]*B[k][j]
        return result
    
    def matrix_scalar_mul(self,A,scalar):
        return [[A[i][j]*scalar for j in range(len(A[0]))] for i in range(len(A))]
    
    

    def matrix_shape(self,matrix):
        
        if isinstance(matrix,list) and all(isinstance(row,list) for row in matrix):
            return (len(matrix), len(matrix[0]) if matrix else 0)
        elif isinstance(matrix,Matrix):
            return (len(matrix.rows), len(matrix.rows[0]) if matrix.rows else 0)
        elif isinstance(matrix,Vector):
            return (1, len(matrix.elements))
        else:
            raise Exception("Input is not a valid matrix or vector")
    
    def matrix_identity(self,n):
        return [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    
    def matrix_zeroes(self,rows,cols):
        return [[0 for _ in range(cols)] for _ in range(rows)]
    

    def matrix_inverse(self,matrix):
        if self.matrix_shape(matrix)[0]!=self.matrix_shape(matrix)[1]:
            raise Exception("Inverse is only defined for square matrices")
        det=self.matrix_determinant(matrix)
        if det==0:
            raise Exception("Matrix is singular and has no inverse")
        
        # gauss jordan elimination method for matrix inversion

        rows,cols=self.matrix_shape(matrix)
        A=matrix
        n = rows

        # Create augmented matrix [A | I]
        I = self.matrix_identity(n)
        augmented = [A[i] + I[i] for i in range(n)]

        # Gauss-Jordan elimination
        for i in range(n):

            # Find pivot
            pivot = augmented[i][i]
            if pivot == 0:
                raise Exception("Matrix is singular (non-invertible)")

            # Normalize pivot row
            for j in range(2*n):
                augmented[i][j] /= pivot

            # Eliminate other rows
            for k in range(n):
                if k != i:
                    factor = augmented[k][i]
                    for j in range(2*n):
                        augmented[k][j] -= factor * augmented[i][j]

        # Extract inverse from right half
        inverse = [row[n:] for row in augmented]
        return inverse    
    
    def matrix_determinant(self,matrix):
        rows,cols=self.matrix_shape(matrix)
        if rows!=cols:
            raise Exception("Determinant is only defined for square matrices")
        
        # conversion from AST Matrix to 2D list if needed
        if isinstance(matrix,Matrix):
            matrix=[[self.interpret(element) for element in row] for row in matrix.rows]
        
        # LU decomposition method for determinant calculation
        n=rows
        A=[row[:] for row in matrix]  # Make a copy of the matrix
        det=1
        for i in range(n):
            # Find pivot
            pivot=i
            for j in range(i+1,n):
                if abs(A[j][i])>abs(A[pivot][i]):
                    pivot=j
            if A[pivot][i]==0:
                return 0  # Singular matrix
            
            # Swap rows if needed
            if pivot!=i:
                A[i],A[pivot]=A[pivot],A[i]
                det*=-1  # Row swap changes sign of determinant
            
            det*=A[i][i]  # Multiply by pivot element
            
            # Eliminate below
            for j in range(i+1,n):
                factor=A[j][i]/A[i][i]
                for k in range(i,n):
                    A[j][k]-=factor*A[i][k]
        return det
    
    
    def matrix_transpose(self,matrix):
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    
    def visit_FunctionDef(self, node):
    
        self.functions[node.name] = node
        print(f"Defined function '{node.name}' with parameters {[param.name for param in node.parameters]}")
    
    def sym_integrate(self,expr, var):
        # sym_expr=self.to_sympy(expr)
        # sym_var=self.to_sympy(var)
        return sp.integrate(expr, var)
    
    def sym_diff(self,expr, var):
        # sym_expr=self.to_sympy(expr)
        # sym_var=self.to_sympy(var)
        return self.sp.diff(expr, var)
    
    def sym_limit(self,expr, var, point):
        # sym_expr=self.to_sympy(expr)
        # sym_var=self.to_sympy(var)
        # sym_point=self.to_sympy(point)
        return self.sp.limit(expr, var, point)
    
    def sym_solve(self,expr, var):
        # sym_expr=self.to_sympy(expr)
        # sym_var=self.to_sympy(var)
        return self.sp.solve(expr, var)
    
    def sym_summation(self,expr, var, start, end):
        # sym_expr=self.to_sympy(expr)
        # sym_var=self.to_sympy(var)
        # sym_start=self.to_sympy(start)
        # sym_end=self.to_sympy(end)
        return self.sp.summation(expr, (var, start, end))
    
    def sym_simplify(self,expr):
        # sym_expr=self.to_sympy(expr)
        return self.sp.simplify(expr)
    def sym_factor(self,expr):
        # sym_expr=self.to_sympy(expr)
        return self.sp.factor(expr)
    
    def np_eigenvalues(self,matrix):
        numpy_matrix=np.array(self.interpret(matrix))
        return np.linalg.eigvals(numpy_matrix)
    
    def np_solve_linear(self,A,b):
        
        row,col=self.matrix_shape(self.interpret(A))
        if row!=col:
            raise Exception("Coefficient matrix A must be square for solve_linear")
        
        if self.matrix_determinant(A)==0:
            raise Exception("Coefficient matrix A is singular, system has no unique solution")

        numpy_A=np.array(self.interpret(A))
        numpy_b=np.array(self.interpret(b))
        return np.linalg.solve(numpy_A, numpy_b)
    
    def np_eigenvectors(self,matrix):
        numpy_matrix=np.array(self.interpret(matrix))
        return np.linalg.eig(numpy_matrix)[1]  # Return eigenvectors only
