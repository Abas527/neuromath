from neuromath.lexer.lexer import Lexer
from neuromath.parser.parser import Parser
from neuromath.interpreter.interpreter import Interpreter
import sympy as sp

def run_test(code):
    print("\n--- Test ---")
    print("Code:\n", code)
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print("Tokens:", tokens)
    
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)
    
    interpreter = Interpreter()
    result = interpreter.interpret(ast)


    if isinstance(result, sp.Expr) and result.free_symbols == set():
        result = result.evalf()
    print("Result of last statement:", result)
    print("Variables:", interpreter.variables)



# # Simple assignment + arithmetic + function
# test1 = "x=2\ny=3\nz=pow(x,y)+sin(pi/2)"
# run_test(test1)

# #  Unary operators
# test2 = "a=5\nb=-a\nc=+a+d"  # d undefined will raise error
# try:
#     run_test(test2)
# except Exception as e:
#     print("Error:", e)

# #  Complex expression
# test3 = "x=2\ny=3\nresult=(x+y)*(x-y)/2"
# run_test(test3)

# #  Matrix
# test4 = "m=[[1,2],[3,4]]\nn=[[5,6],[7,8]]\nr=m"  # simple assignment of matrix
# run_test(test4)

# #  Mixed arithmetic and function calls
# test5 = "x=2\ny=3\nz=pow(x,y)+sqrt(y)"
# run_test(test5)


# #  Single expression
# test6 = "42.5 + 58"
# run_test(test6)

#self.symbolic_functions={"integrate","diff","limit","solve","summation","simplify","factor","eigenval","solve_linear","eigenvec"}


test7='x=3\nf(x)=x^2+3*x\nprint(diff(f(x),x))'
run_test(test7)

# test8="factor(x**2 - 5*x + 6)"
# run_test(test8)