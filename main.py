import sys
from neuromath.lexer.lexer import Lexer
from neuromath.parser.parser import Parser
from neuromath.interpreter.interpreter import Interpreter


def main():
    print("NeuroMath CLI (type 'exit' to quit)")

    interpreter = Interpreter()

    while True:
        try:
            text = input(">>> ")

            if text.strip().lower() == "exit":
                break

            lexer = Lexer(text)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            result = interpreter.interpret(ast)

            if result is not None:
                print(result)

        except Exception as e:
            print("Error:", e)


def run():
    main()


if __name__ == "__main__":
    main()