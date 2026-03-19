import math
import random
import numpy as np
import sympy as sp
from neuromath.lexer.token_types import TokenType
from neuromath.parser.ast_nodes import *

class Interpreter:
    def __init__(self,variables=None,functions=None):
        self.sp=sp
        self.np=np
        self.variables =variables if variables is not None else {
            "pi": float(sp.pi),
            "e": float(sp.E),
        }

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
        self.numeric_functions={
            "sin":np.sin,
            "cos":np.cos,
            "tan":np.tan,
            "arcsin":np.arcsin,
            "arccos":np.arccos,
            "arctan":np.arctan,
            "log":np.log,
            "ln":np.log,
            "exp":np.exp,
            "sqrt":np.sqrt,
            "abs":np.abs,
            "pow":np.power,

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
            "num":self.to_numeric,
            "random_vector":self.random_vector,
            "random_matrix":self.random_matrix,
            "random":self.random_number,
            "sum":self.sum,
            "svd":self.svd,
            "rank":self.rank,
            "trace":self.trace,
            "sigmoid":self.sigmoid,
            "relu":self.relu,
            "softmax":self.softmax,
            "tanh":self.tanh,
            "mean":self.mean,
            "median":self.median,
            "std":self.std,
            "cov":self.cov,
            "corr":self.corr,

            # symbolic math functions
            "integrate":self.sym_integrate,
            "diff":self.sym_diff,
            "limit":self.sym_limit,
            "solve":self.sym_solve,
            "summation":self.sym_summation,
            "simplify":self.sym_simplify,
            "factor":self.sym_factor,
            "explain":self.sym_explain,
            "eigenval":self.np_eigenvalues,
            "solve_linear":self.np_solve_linear,
            "eigenvec":self.np_eigenvectors,
            "plot":self.plot,
            "plot_surface":self.plot_surface,
            "plot_vector":self.plot_vector,
            "plot3d":self.plot3d,
            "gradient":self.gradient,
            "gradient_descent":self.gradient_descent


        }
        self.symbolic_functions={"integrate","gradient","gradient_descent","explain","diff","limit","solve","summation","simplify","factor"}
    
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
            if node.name in self.variables:
                return sp.Number(self.variables[node.name])
            return sp.Symbol(node.name)
        elif isinstance(node,Number):
            return sp.Number(node.value)
        elif isinstance(node,UnaryOp):
            operand=self.to_sympy(node.operand,symbolic_mode)
            if node.op==TokenType.PLUS:
                return operand
            elif node.op==TokenType.MINUS:
                return -operand
            else:
                raise Exception(f"Unknown unary operator '{node.op}'")
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

            # special case for plot function
            
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
        print(self.variables)
        if node.name in self.variables:
            return self.variables[node.name]
        else:
            raise Exception(f"Undefined variable '{node.name}'")
        
    def visit_UnaryOp(self,node:UnaryOp):
        operand=self.interpret(node.operand)
        if node.op==TokenType.PLUS:
            return +operand
        elif node.op==TokenType.MINUS:
            return -operand
        else:
            raise Exception(f"Unknown unary operator '{node.op}'")
    
    def visit_BinaryOp(self,node:BinaryOp):
        left=node.left
        right=node.right

        left=self.interpret(left)
        right=self.interpret(right)

        if (isinstance(left,Vector)) and (isinstance(right,Vector)):
            if node.op==TokenType.PLUS:
                return self.vector_add(left,right)
            elif node.op==TokenType.MINUS:
                return self.vector_sub(left,right)
            elif node.op==TokenType.MUL:
                return self.vector_mul(left,right)
            else:
                raise Exception(f"Unsupported operator '{node.op}' for vectors")
        elif isinstance(right,Vector) and isinstance(left,(int,float)) or isinstance(right,(int,float)) and isinstance(left,Vector):
            if node.op==TokenType.MUL:
                return self.scalar_vector_mul(right,left)
            elif node.op==TokenType.DIV:
                return self.scalar_vector_div(right,left)
            elif node.op==TokenType.PLUS:
                return self.scalar_vector_add(right,left)
            elif node.op==TokenType.MINUS:
                return self.scalar_vector_sub(right,left)
            else:
                raise Exception(f"Unsupported operator '{node.op}' for scalar-vector multiplication")
        
        elif isinstance(left,Matrix) and isinstance(right,Matrix):
            if node.op==TokenType.PLUS:
                return self.matrix_add(left,right)
            elif node.op==TokenType.MINUS:
                return self.matrix_sub(left,right)
            elif node.op==TokenType.MUL:
                return self.matrix_mul(left,right)
            else:
                raise Exception(f"Unsupported operator '{node.op}' for matrices")
        elif (isinstance(right,Matrix) and isinstance(left,(int,float))):
            if node.op==TokenType.MUL:
                return self.matrix_scalar_mul(right,left)
            else:
                raise Exception(f"Unsupported operator '{node.op}' for matrix-scalar multiplication")
        elif isinstance(left,Matrix) and isinstance(right,Vector):
            
            if node.op==TokenType.MUL:
                return self.matrix_vector_mul(left,right)
            else:
                raise Exception(f"Unsupported operator '{node.op}' for matrix-vector multiplication")

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


    def to_numeric(self, val):

        import sympy as sp

        # Direct numeric types
        if isinstance(val, (int, float)):
            return float(val)

        # SymPy numbers
        if isinstance(val, sp.Number):
            return float(val)

        # Infinity handling
        if val in (sp.oo, -sp.oo, sp.zoo):
            return float("inf")

        # Symbol handling
        if isinstance(val, sp.Symbol):
            name = str(val)

            if name in self.variables:
                return float(self.variables[name])
            else:
                raise Exception(f"Undefined variable '{name}'")

        # General SymPy expressions
        if isinstance(val, sp.Expr):
            if val.free_symbols:
                val = val.subs(self.variables)

            val = sp.N(val, 15)
            try:
                return float(val)

            except Exception as e:
                raise Exception(f"Cannot convert expression '{val}' to float")

        # fallback
        return float(val)
    def plot_vector(self,node):

        x=node.arguments[0]
        y=node.arguments[1]
        is_line=self.interpret(node.arguments[2])

        import plotly.graph_objects as go
        import numpy as np

        fig=go.Figure()


        if isinstance(x,Vector) and isinstance(y,Vector):
            x=[self.interpret(e) for e in x.elements]
            y=[self.interpret(e) for e in y.elements]
        elif isinstance(x,Vector) and isinstance(y,Matrix):
            x=[self.interpret(e) for e in x.elements]
        elif isinstance(x,Identifier) and isinstance(y,Identifier):
            if x.name in self.variables and y.name in self.variables:
                x=self.variables[x.name]
                y=self.variables[y.name]
                x=self.vector_to_list(x)
                y=self.vector_to_list(y)
        elif isinstance(x,Identifier) and isinstance(y,Vector):
            if x.name in self.variables:
                x=self.variables[x.name]
                x=self.vector_to_list(x)
            y_vars=self.vector_to_list(self.interpret(y))
            # plot multiple lines with respect to x
            if is_line==1:
                def_mode="lines"
            else:
                def_mode="markers"
            count=0
            for y in y_vars:
                y=self.vector_to_list(y)
                if count==len(y_vars)-1:
                    def_mode="lines"
                fig.add_trace(go.Scatter(x=x, y=y, mode=def_mode))
                count+=1
            return fig
        else:
            raise Exception("Both x and y must be vectors")
        
        if is_line==1:
            fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="lines")])
        else:

            fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="markers")])
        return fig


        

    def manage_plot(self,node):

        expr_node = node.arguments[0]
        if isinstance(expr_node, Vector):
            exprs = [self.to_sympy(e, symbolic_mode=True) for e in expr_node.elements]
        else:
            exprs = [self.to_sympy(expr_node, symbolic_mode=True)]

        var_set = set()
        for expr in exprs:
            var_set.update(expr.free_symbols)
        vars_list = list(var_set)
        num_vars = len(vars_list)

        if num_vars == 1:
            sym_var = sp.Symbol(node.arguments[1].name)

        # Interpret bounds
            start = self.to_numeric(self.interpret(node.arguments[2]))
            end = self.to_numeric(self.interpret(node.arguments[3]))

        # Call plot for all expressions
            return self.plot(exprs, sym_var, start, end)

        elif num_vars == 2:
            sym_x_var, sym_y_var = node.arguments[1].name, node.arguments[2].name
            sym_x_var, sym_y_var = sp.Symbol(sym_x_var), sp.Symbol(sym_y_var)

        # Interpret bounds
            start_x = self.to_numeric(self.interpret(node.arguments[3]))
            end_x = self.to_numeric(self.interpret(node.arguments[4]))
            start_y = self.to_numeric(self.interpret(node.arguments[5]))
            end_y = self.to_numeric(self.interpret(node.arguments[6]))


        # Call surface plot for all expressions
            return self.plot_surface(exprs, sym_x_var, sym_y_var, start_x, end_x, start_y, end_y)
        elif num_vars==3:
            sym_x_var, sym_y_var, sym_z_var = node.arguments[1].name, node.arguments[2].name, node.arguments[3].name
            sym_x_var, sym_y_var, sym_z_var = sp.Symbol(sym_x_var), sp.Symbol(sym_y_var), sp.Symbol(sym_z_var)
            start_x = self.to_numeric(self.interpret(node.arguments[4]))
            end_x = self.to_numeric(self.interpret(node.arguments[5]))
            start_y = self.to_numeric(self.interpret(node.arguments[6]))
            end_y = self.to_numeric(self.interpret(node.arguments[7]))
            start_z = self.to_numeric(self.interpret(node.arguments[8]))
            end_z = self.to_numeric(self.interpret(node.arguments[9]))
            return self.plot3d(exprs, sym_x_var, sym_y_var, sym_z_var, start_x, end_x, start_y, end_y, start_z, end_z)
        else:
            raise Exception(
                f"Invalid number of variables ({num_vars}) for plot function. Only 1D or 2D or 3D supported."
            )
    def visit_FunctionCall(self, node: FunctionCall):

        #special case for plot function
        if node.name=="plot":
            return self.manage_plot(node)
        if node.name=="plot3d":
            return self.manage_plot(node)
        
        if node.name=="plot_surface":
            return self.manage_plot(node)
        if node.name=="plot_vector":
            return self.plot_vector(node)
        if node.name=="gradient_descent":
            return self.manage_gradient(node)

            

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
            try:
                args = [self.interpret(arg) for arg in node.arguments]
                return self.numeric_functions[node.name](*args)
            except:
                args = [self.to_sympy(arg,symbolic_mode=True) for arg in node.arguments]
                return self.math_functions[node.name](*args)

        else:
            raise Exception(f"Undefined function '{node.name}'")
    
    def call_user_function(self,func,args):
        
        # check arity
        if len(args)!=len(func.parameters):
            raise Exception(f"Expected {len(func.parameters)} arguments but got {len(args)}")
        
        is_vector=any(isinstance(arg,Vector) for arg in args)

        if is_vector:

            lengths=[self.matrix_shape(arg)[1] for arg in args]
            if not all(length==lengths[0] for length in lengths):
                raise Exception("All vectors must have the same length")
            
            results=[]
            for i in range(lengths[0]):
                old_variables=self.variables.copy()
                for param,arg in zip(func.parameters,args):
                    arg=self.vector_to_list(arg)
                    if isinstance(arg,list):
                        self.variables[param.name]=arg[i]
                    else:
                        self.variables[param.name]=arg
                results.append(self.interpret(func.body))
                self.variables=old_variables
            return Vector(results)
        else:
            old_variable=self.variables.copy()

            for param, arg in zip(func.parameters, args):
                self.variables[param.name]=arg

            result=self.interpret(func.body)
            self.variables=old_variable
            return result
    
    def scalar_or_vector(self,node1,node2):
        if isinstance(node1,Vector):
            return self.vector_to_list(node1),node2
        else:
            return self.vector_to_list(node2),node1

    def scalar_vector_mul(self,vector,scale):
        vector,scale=self.scalar_or_vector(vector,scale)
        return Vector([scale*element for element in vector])
    def scalar_vector_div(self,vector,scale):
        vector,scale=self.scalar_or_vector(vector,scale)
        return Vector([element/scale for element in vector])
    def scalar_vector_add(self,vector,scale):
        vector,scale=self.scalar_or_vector(vector,scale)
        print(type(vector),type(scale))
        return Vector([element+scale for element in vector])
    def scalar_vector_sub(self,vector,scale):
        vector,scale=self.scalar_or_vector(vector,scale)
        return Vector([element-scale for element in vector])

    def visit_Matrix(self,node):
        matrix=[]
        for row in node.rows:
            matrix.append([self.interpret(element) for element in row])
        return Matrix(matrix)
    def random_number(self,start=0,end=100):
        return random.randint(start,end)
    def random_vector(self,n,start=0,end=100):
        return Vector([random.randint(start,end) for _ in range(n)])  
    def random_matrix(self,m,n,start=0,end=100):
        return Matrix([[random.randint(start,end) for _ in range(n)] for _ in range(m)])
    def visit_Vector(self,node):
        return Vector([self.interpret(element) for element in node.elements])
    
    def vector_to_list(self,vector):
        return [element for element in vector.elements]
    
    def matrix_to_list(self,matrix):
        return [[element for element in row] for row in matrix.rows]
    
    def matrix_vector_mul(self,A,v):
        A=self.matrix_to_list(A)
        v=self.vector_to_list(v)
        return Matrix([sum(A[i][j]*v[j] for j in range(len(A[0]))) for i in range(len(A))])

    def vector_add(self,v1,v2):
        v1=self.vector_to_list(v1)
        v2=self.vector_to_list(v2)
        if len(v1)!=len(v2):
            raise Exception("Vectors must have the same length for addition")
        return Vector([v1[i]+v2[i] for i in range(len(v1))])
    def vector_mul(self,v1,v2):
        v1=self.vector_to_list(v1)
        v2=self.vector_to_list(v2)

        if len(v1)!=len(v2):
            raise Exception("Vectors must have the same length for multiplication")
        return Vector([v1[i]*v2[i] for i in range(len(v1))])
    def vector_sub(self,v1,v2):
        v1=self.vector_to_list(v1)
        v2=self.vector_to_list(v2)
        if len(v1)!=len(v2):
            raise Exception("Vectors must have the same length for subtraction")
        print(type(v1),type(v2))
        return Vector([v1[i]-v2[i] for i in range(len(v1))])
    
    def matrix_add(self,A,B):
        A,B=self.matrix_to_list(A),self.matrix_to_list(B)
        if self.matrix_shape(A)!=self.matrix_shape(B):
            raise Exception("Matrices must have the same shape for addition")
        return Matrix([
            [A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A)) ])
    
    def dot_product(self,v1,v2):
        v1=self.vector_to_list(v1)
        v2=self.vector_to_list(v2)
        if len(v1)!=len(v2):
            raise Exception("Vectors must have the same length for dot product")
        return sum(v1[i]*v2[i] for i in range(len(v1)))
    
    def cross_product(self,v1,v2):
        v1=self.vector_to_list(v1)
        v2=self.vector_to_list(v2)
        if len(v1)!=3 or len(v2)!=3:
            raise Exception("Cross product is only defined for 3D vectors")
        return Vector([
            v1[1]*v2[2]-v1[2]*v2[1],
            v1[2]*v2[0]-v1[0]*v2[2],
            v1[0]*v2[1]-v1[1]*v2[0]
        ])
    def norm(self,v):
        v=self.vector_to_list(v)
        return math.sqrt(sum(elem**2 for elem in v))
    
    def unit_vector(self,v):
        v=self.vector_to_list(v)
        n=self.norm(v)
        if n==0:
            raise Exception("Cannot compute unit vector of zero vector")
        return Vector([elem/n for elem in v])
    def matrix_sub(self,A,B):
        A,B=self.matrix_to_list(A),self.matrix_to_list(B)
        if self.matrix_shape(A)!=self.matrix_shape(B):
            raise Exception("Matrices must have the same shape for subtraction")
        return Matrix([
            [A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A)) ])
    
    def matrix_mul(self,A,B):
        A,B=self.matrix_to_list(A),self.matrix_to_list(B)
        if self.matrix_shape(A)[1]!=self.matrix_shape(B)[0]:
            raise Exception("Number of columns in A must equal number of rows in B for multiplication")
        result=[[0 for _ in range(self.matrix_shape(B)[1])] for _ in range(self.matrix_shape(A)[0])]  # Initialize result matrix with zeros
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j]+=A[i][k]*B[k][j]
        return Matrix(result)
    
    def matrix_scalar_mul(self,A,scalar):
        A=self.matrix_to_list(A)
        return Matrix([[A[i][j]*scalar for j in range(len(A[0]))] for i in range(len(A))])
    
    

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
        return Matrix([[1 if i==j else 0 for j in range(n)] for i in range(n)])
    
    def matrix_zeroes(self,rows,cols):
        return Matrix([[0 for _ in range(cols)] for _ in range(rows)])
    

    def matrix_inverse(self,matrix):
        matrix=self.matrix_to_list(matrix)
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
        return Matrix(inverse)    
    
    def matrix_determinant(self,matrix):
        matrix=self.matrix_to_list(matrix)
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
        matrix=self.matrix_to_list(matrix)
        return Matrix([[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))])
    
    def visit_FunctionDef(self, node):
    
        self.functions[node.name] = node
        print(f"Defined function '{node.name}' with parameters {[param.name for param in node.parameters]}")
    
    def sym_integrate(self,expr, var):
        return sp.integrate(expr, var)
    
    def sym_diff(self,expr, var):
        return self.sp.diff(expr, var)
    
    def sym_limit(self,expr, var, point):
        return self.sp.limit(expr, var, point)
    
    def sym_solve(self,expr, var):
        return self.sp.solve(expr, var)
    
    def sym_summation(self,expr, var, start, end):
        return self.sp.summation(expr, (var, start, end))
    
    def sym_explain(self,expr):


        # check free symbols
        var_list=list(expr.free_symbols)

        if not var_list:
            return f"Expression {expr} is constant"
        
        if len(var_list)>1:
            return f"Expression {expr} has multiple variables: {var_list}"
        
        var=var_list[0]
        
        result={}
        result["function"]=self.sp.simplify(expr)
        result["derivative"]=self.sp.diff(expr,var)
        result["integral"]=self.sp.integrate(expr,var)
        result["limit->0"]=self.sp.limit(expr,var,0)
        result["solve"]=self.sp.solve(expr,var)
        result["factor"]=self.sp.factor(expr)
        result["series"]=self.sp.series(expr,var)

        result["critical_points"]=self.sp.solve(self.sp.diff(expr,var),var)
        
        result["second_derivative"]=self.sp.diff(self.sp.diff(expr,var),var)
        result["inflection_point"]=sp.solve(self.sp.diff(self.sp.diff(expr,var),var),var)

        start_point=min(result["critical_points"] if result["critical_points"] else [-50])
        end_point=max(result["critical_points"] if result["critical_points"] else [50])

        if isinstance(result["derivative"],sp.Number):
            fig=self.plot(result["function"],var,start_point,end_point,False)
        elif isinstance(result["second_derivative"],sp.Number):
            fig=self.plot([result["function"],result["derivative"]],var,start_point,end_point,False)
        else:
            fig=self.plot([result["function"],result["derivative"],result["second_derivative"]],var,start_point,end_point,False)

        output=f"""
Expression: {expr} \n

Function: {result["function"]} \n
Derivative: {result["derivative"]} \n
Integral: {result["integral"]} \n 
Limit -> 0: {result["limit->0"]} \n
Solve: {result["solve"]} \n
Factor: {result["factor"]} \n
Series: {result["series"]} \n

Critical Points: {result["critical_points"]} \n
Second Derivative: {result["second_derivative"]} \n
Inflection Point: {result["inflection_point"]} \n
"""

        return output

    def gradient(self,expr):
        
        vars=list(expr.free_symbols)
        grad=[]

        for var in vars:
            grad.append(self.sp.diff(expr,var))
        
        return grad
    
    def manage_gradient(self,node):
        expr=self.to_sympy(node.arguments[0],symbolic_mode=True)
        if isinstance(node.arguments[1],Vector):
            vars=Vector([self.to_sympy(v,symbolic_mode=True) for v in node.arguments[1].elements])
        else:
            vars=self.to_sympy(node.arguments[1],symbolic_mode=True)
        if isinstance(node.arguments[2],Vector):
            start=Vector([self.to_sympy(v,symbolic_mode=True) for v in node.arguments[2].elements])
        else:
            start=self.to_sympy(node.arguments[2],symbolic_mode=True)
        steps=self.interpret(node.arguments[3])
        lr=self.interpret(node.arguments[4]) if len(node.arguments)>4 else 0.1

        return self.gradient_descent(expr,vars,start,steps,lr)


    def gradient_descent(self,expr,var,start,steps,lr=0.1):

        if isinstance(var,Vector):
            vars=self.vector_to_list(var)
            starts=self.vector_to_list(start)
            gradients=self.gradient(expr)
            if len(vars)!=len(gradients):
                raise Exception("Number of variables and gradients must be equal")

            for j in range(steps):
                
                for i in range(len(vars)):
                    gr_val=gradients[i].subs(vars[i],starts[i])
                    starts[i]=starts[i]-lr*gr_val
            return Vector(starts)
        else:
            var_start=start
            gradeint=self.sp.diff(expr,var)
            for i in range(steps):
                gr_val=gradeint.subs(var,start)
                start=start-lr*gr_val

            return start


             



    def sym_simplify(self,expr):
        return self.sp.simplify(expr)
    def sym_factor(self,expr):
        return self.sp.factor(expr)
    
    def np_eigenvalues(self,matrix):
        matrix=self.matrix_to_list(matrix)

        numpy_matrix=np.array(matrix)
        return Vector(np.linalg.eigvals(numpy_matrix))
    
    def np_solve_linear(self,A,b):
        A=self.matrix_to_list(A)
        b=self.vector_to_list(b)
        row,col=self.matrix_shape(A)
        if row!=col:
            raise Exception("Coefficient matrix A must be square for solve_linear")
        
        if self.matrix_determinant(A)==0:
            raise Exception("Coefficient matrix A is singular, system has no unique solution")

        numpy_A=np.array(A)
        numpy_b=np.array(b)
        return Vector(np.linalg.solve(numpy_A, numpy_b))
    
    def np_eigenvectors(self,matrix):
        matrix=self.matrix_to_list(matrix)
        numpy_matrix=np.array(matrix)
        return Vector(np.linalg.eig(numpy_matrix)[1])  # Return eigenvectors only
    
    def plot(self,exprs,var,start,end,ishow=False,num_points=1000):
        import plotly.graph_objects as go
        import numpy as np
        from sympy import lambdify,Symbol
        

        if not isinstance(var,Symbol):
            var=Symbol(var)


        if not isinstance(exprs,list):
            ex=[exprs]
        else:
            ex=exprs

        num_points=int(num_points)
        start,end=self.to_numeric(start),self.to_numeric(end)
        
        fig = go.Figure()
        
        for expr in ex:
            # Convert symbolic expr to numeric function
            f_numeric = lambdify(var, expr, modules=["numpy"])
            x_vals = np.linspace(start, end, num_points)
            y_vals = f_numeric(x_vals)            

            # Add trace
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name=str(expr)))

            fig.update_layout(
                title="Function Plot",
                xaxis_title=str(var),
                yaxis_title="f({})".format(var),
                template="plotly_white"
            )
        
        if ishow:
            fig.show()

        return fig

    def plot_surface(self,exprs, var1, var2, start1, end1, start2, end2, num_points=100):
        import plotly.graph_objects as go
        import numpy as np
        from sympy import lambdify, Symbol

        if not isinstance(var1, Symbol):
            var1 = Symbol(var1)

        if not isinstance(var2, Symbol):
            var2 = Symbol(var2)
        num_points=int(num_points)

    # Generate x and y values
        start1,end1,start2,end2=self.to_numeric(start1),self.to_numeric(end1),self.to_numeric(start2),self.to_numeric(end2)
        x_vals = np.linspace( start1, end1 ,num_points)
        y_vals = np.linspace( start2, end2 ,num_points)
        x, y = np.meshgrid(x_vals, y_vals)

    # Create Plotly figure
        fig = go.Figure()

        for expr in exprs:
        # Convert symbolic expr to numeric function
            f_numeric = lambdify((var1, var2), expr, modules=["numpy"])
            z_vals = f_numeric(x, y)

        # Add trace
            fig.add_trace(go.Surface(z=z_vals, x=x, y=y, name=str(expr)))

            fig.update_layout(
                title="Function Plot",
                scene=dict(
                    xaxis_title=str(var1),
                    yaxis_title=str(var2),
                    zaxis_title="f({},{})".format(var1, var2),
            ),
            template="plotly_white",
        )

        return fig

    def plot3d(self, exprs, var1, var2, var3,
               start1, end1, start2, end2, start3, end3,
               num_points=30, num_slices=10):

        import plotly.graph_objects as go
        import numpy as np
        from sympy import lambdify, Symbol

    # --- Ensure symbols ---
        var1 = Symbol(var1) if not isinstance(var1, Symbol) else var1
        var2 = Symbol(var2) if not isinstance(var2, Symbol) else var2
        var3 = Symbol(var3) if not isinstance(var3, Symbol) else var3

    # --- Convert bounds ---
        start1, end1 = self.to_numeric(start1), self.to_numeric(end1)
        start2, end2 = self.to_numeric(start2), self.to_numeric(end2)
        start3, end3 = self.to_numeric(start3), self.to_numeric(end3)

        num_points = int(num_points)
        num_slices = int(num_slices)

    # --- Generate 2D grid (x, y only) ---
        x_vals = np.linspace(start1, end1, num_points)
        y_vals = np.linspace(start2, end2, num_points)
        x, y = np.meshgrid(x_vals, y_vals)

    # --- Slice values along z ---
        z_slices = np.linspace(start3, end3, num_slices)

        fig = go.Figure()

        for expr in exprs:
            f_numeric = lambdify((var1, var2, var3), expr, modules=["numpy"])

            all_x, all_y, all_z, all_vals = [], [], [], []

            for z_val in z_slices:
                z_plane = np.full_like(x, z_val)

                vals = f_numeric(x, y, z_val)  # ⚡ only 2D computation

                all_x.append(x)
                all_y.append(y)
                all_z.append(z_plane)
                all_vals.append(vals)

        # --- Stack slices ---
            X = np.stack(all_x, axis=2)
            Y = np.stack(all_y, axis=2)
            Z = np.stack(all_z, axis=2)
            V = np.stack(all_vals, axis=2)

            fig.add_trace(go.Isosurface(
                x=X.flatten(),
                y=Y.flatten(),
                z=Z.flatten(),
                value=V.flatten(),
                name=str(expr),
                surface_count=4,
                caps=dict(x_show=False, y_show=False)
            ))

        fig.update_layout(
            title="3D Function Plot (Sliced)",
            scene=dict(
                xaxis_title=str(var1),
                yaxis_title=str(var2),
                zaxis_title=str(var3),
                aspectratio=dict(x=1, y=1, z=1),
            ),
            template="plotly_white"
        )

        return fig
    def sum(self,v1):
        v1=self.np.array(self.vector_to_list(v1))
        return self.np.sum(v1)
    def mean(self,v1):
        v1=self.np.array(self.vector_to_list(v1))
        return self.np.mean(v1)
    def median(self,v1):
        v1=self.np.array(self.vector_to_list(v1))
        return self.np.median(v1)
    def std(self,v1):
        v1=self.np.array(self.vector_to_list(v1))
        return self.np.std(v1)
    def cov(self,v1,v2):
        v1=self.np.array(self.vector_to_list(v1))
        v2=self.np.array(self.vector_to_list(v2))
        return Matrix(self.np.cov(v1,v2))
    def corr(self,v1,v2):
        v1=self.np.array(self.vector_to_list(v1))
        v2=self.np.array(self.vector_to_list(v2))
        return Matrix(self.np.corrcoef(v1,v2))
    def sigmoid(self,x):
        x=self.to_numeric(x)
        return 1 / (1 + self.np.exp(-x))
    
    def relu(self,x):
        x=self.to_numeric(x)
        return self.np.maximum(0, x)
    
    def softmax(self,x):
        if isinstance(x,Vector):
            x=self.np.array(self.vector_to_list(x))
            return Vector(self.np.exp(x) / self.np.sum(self.np.exp(x)))
        else:
            raise Exception("Input must be a vector")
    
    def tanh(self,x):
        x=self.to_numeric(x)
        return (self.np.exp(x) - self.np.exp(-x)) / (self.np.exp(x) + self.np.exp(-x))
    
    def rank(self,A):
        A=self.np.array(self.matrix_to_list(A))
        return self.np.linalg.matrix_rank(A)
    
    def trace(self,A):
        A=self.np.array(self.matrix_to_list(A))
        return self.np.trace(A)
    
    def svd(self,A):
        A=self.np.array(self.matrix_to_list(A))
        return self.np.linalg.svd(A)

        