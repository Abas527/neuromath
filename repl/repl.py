from neuromath.lexer.lexer import Lexer
from neuromath.parser.parser import Parser
from neuromath.interpreter.interpreter import Interpreter
from neuromath.semantic.analyzer import SemanticAnalyzer

def repl():
    print("=== NeuroMath REPL ===")
    print("Type 'exit' to quit.\n")
    
    interpreter = Interpreter()  # single interpreter instance

    while True:
        try:
            text = input(">>> ").strip()
            if text.lower() in ("exit", "quit"):
                break
            if not text:
                continue

            # Lexing
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            # Semantic Analysis
            # analyzer = SemanticAnalyzer()
            # analyzer.analyze(ast)
            # Interpretation
            result = interpreter.interpret(ast)
            
            if result is not None:
                print(result)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    repl()