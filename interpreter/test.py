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





# 0
# test0="y=sqrt(5)\na=num(y)\nb=num((1+a)/2)\nc=num((1-a)/2)\nf(x)=(b^x-c^x)/a\nplot(f(x),x,0,10)"
# run_test(test0)

# 1
# test1="v=[1,2,3]\nw=[4,5,6]\nf(x,y,z)=x^2+y^2+z^2\nf(2,3,4)\n"
# run_test(test1)

# # 2
# test2="v=[1,2,3]\n w=[-1,-2,-3]\n v+w"
# run_test(test2)

# # 3
# test3="v=[1,2,3]\n dot(v,v)"
# run_test(test3)

# # 4
# test4="A=[[1,2],[3,4]]\n B=[[5,6],[7,8]]\n A+B\n A*B"
# run_test(test4)

# # 5
# test5="A=[[1,2],[3,4]]\n 5*A"
# run_test(test5)

# # 6
# test6="x=3\n v=[x,x^2,x^3]"
# run_test(test6)

# # 7
# test7="x=2\n A=[[x,x^2],[x^3,x^4]]"
# run_test(test7)

# # 8
# test8="pi"
# run_test(test8)

# # 9
# test9="f(x)=sin(x)+cos(x)\n plot(f(x),x,-6.28,6.28)"
# run_test(test9)

# # 10
# test10="f(x)=exp(-x^2)\n plot(f(x),x,-5,5)"
# run_test(test10)

# # 11
# test11="f(x)=x^2\n g(x)=x^3\n plot([f(x),g(x)],x,-5,5)"
# run_test(test11)

# # 12
# test12="f(x,y)=x^2+y^2\n plot_surface(f(x,y),x,y,-10,10,-10,10)"
# run_test(test12)

# # 13
# test13="f(x,y)=x^2-y^2\n plot_surface(f(x,y),x,y,-10,10,-10,10)"
# run_test(test13)

# # 14
# test14="f(x,y)=sin(x*y)\n plot_surface(f(x,y),x,y,-6.28,6.28,-6.28,6.28)"
# run_test(test14)

# # 15
# test15="f(x,y)=exp(-(x^2+y^2))\n plot_surface(f(x,y),x,y,-5,5,-5,5)"
# run_test(test15)

# # 16
# test16="f(x,y)=x^2+y^2\n g(x,y)=-x^2-y^2\n plot_surface([f(x,y),g(x,y)],x,y,-10,10,-10,10)"
# run_test(test16)

# # 17
# test17="f(x,y)=x^3-y^3\n g(x,y)=sin(x)+cos(y)\n plot_surface([f(x,y),g(x,y)],x,y,-5,5,-5,5)"
# run_test(test17)

# # 18
# test18="f(x,y)=sin(x^2+y^2)+cos(x*y)\n plot_surface(f(x,y),x,y,-5,5,-5,5)"
# run_test(test18)

# # 19
# test19="f(x,y)=x*y\n plot_surface(f(x,y),x,y,-20,20,-20,20)"
# run_test(test19)

# # 20
# test20="f(x)=x^10-x^5+x\n plot(f(x),x,-5,5)"
# run_test(test20)

# # 21
# test21="f(x)=[x,x^2,x^3]\n f(3)"
# run_test(test21)

# # 22
# test22="f(x)=[[x,x^2],[x^3,x^4]]\n f(2)"
# run_test(test22)

# # 23
# test23="x=2\n y=3\n f(x,y)=x^2+y^2\n f(x,y)"
# run_test(test23)

# # 24
# test24="v=[1,2,3]\n A=[[1,0,0],[0,1,0],[0,0,1]]\n A*v"
# run_test(test24)

# # 25
# test25="v=[1,2]\n w=[3,4]\n dot(v,w)"
# run_test(test25)

# # 26
# test26="A=[[1,2],[3,4]]\n B=[[2,0],[0,2]]\n A*B+B*A"
# run_test(test26)

# # 27
# test27="f(x)=sin(x)^2+cos(x)^2\n plot(f(x),x,-10,10)"
# run_test(test27)

# # 28
# test28="f(x,y)=sin(x)^2+cos(y)^2\n plot_surface(f(x,y),x,y,-6.28,6.28,-6.28,6.28)"
# run_test(test28)

# # 29
# test29="f(x,y)=x^2+y^2+x*y\n plot_surface(f(x,y),x,y,-10,10,-10,10)"
# run_test(test29)

# # 30
# test30="f(x)=1/(x^2+1)\n plot(f(x),x,-20,20)"
# run_test(test30)

# # 31
# test31="f(x)=abs(x)\n plot(f(x),x,-10,10)"
# run_test(test31)

# # 32
# test32="f(x,y)=abs(x*y)\n plot_surface(f(x,y),x,y,-5,5,-5,5)"
# run_test(test32)

# # 33
# test33="f(x)=x\n plot(f(x),x,0,0)"
# run_test(test33)

# # 34
# test34="f(x,y)=x+y\n plot_surface(f(x,y),x,y,1,1,2,2)"
# run_test(test34)

# # 35
# test35="f(x)=sin(x^3)+cos(x^2)\n plot(f(x),x,-5,5)"
# run_test(test35)

# # 36
# test36="f(x,y)=sin(x^2+y^2)+exp(-x*y)\n plot_surface(f(x,y),x,y,-5,5,-5,5)"
# run_test(test36)

# # 37
# test37="v=[sin(1),cos(1),tan(1)]"
# run_test(test37)

# # 38
# test38="A=[[sin(1),cos(1)],[tan(1),exp(1)]]"
# run_test(test38)

# # 39
# test39="f(x)=x^2\n g(x)=f(x)+x\n plot(g(x),x,-10,10)"
# run_test(test39)

# # 40
# test40="f(x,y)=x^2+y^2\n h(x,y)=f(x,y)+x*y\n plot_surface(h(x,y),x,y,-10,10,-10,10)"
# run_test(test40)

# # 41
# test41="f(x)=x^2\n x=5\n f(3)"
# run_test(test41)

# # 42
# test42="f(x,y)=x*y\n x=2\n y=3\n f(x,y)"
# run_test(test42)

# # 43
# test43="f(x)=x^3\n plot(f(x),x,-100,100)"
# run_test(test43)

# # 44
# test44="f(x,y)=x^2-y^2\n plot_surface(f(x,y),x,y,-100,100,-100,100)"
# run_test(test44)

# # 45
# test45="v=[1,2,3]\n w=[4,5,6]\n u=v+w\n dot(u,v)"
# run_test(test45)

# # 46
# test46="A=[[1,2],[3,4]]\n B=[[5,6],[7,8]]\n C=A*B\n C*A"
# run_test(test46)

# # 47
# test47="f(x)=x^2\n g(x)=x^3\n h(x)=f(x)+g(x)\n plot(h(x),x,-5,5)"
# run_test(test47)

# # 48
# test48="f(x,y)=x^2+y^2\n g(x,y)=sin(x*y)\n h(x,y)=f(x,y)+g(x,y)\n plot_surface(h(x,y),x,y,-5,5,-5,5)"
# run_test(test48)

# # 49
# test49="f(x)=exp(sin(x^2))\n plot(f(x),x,-5,5)"
# run_test(test49)

# # 50
# test50="f(x,y)=exp(sin(x^2+y^2))+cos(x*y)\n plot_surface(f(x,y),x,y,-5,5,-5,5)"
# run_test(test50)


#51
# test51="y=[45,70,100,60,90,110]\n x=[1400,400,50,1000,300,60] \ny_cap=[600.0, 200.0, 60.0, 440.0, 160.0, 64.0]\n plot_vector(x,[y,y_cap],0)"
# run_test(test51)

#52 plot 3d functions
test52="f(x,y,z)=x^2+y^2+z^2\n plot3d(f(x,y,z),x,y,z,-10,10,-10,10,-10,10)"
run_test(test52)