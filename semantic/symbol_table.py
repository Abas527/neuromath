class SymbolTable:
    def __init__(self):
        self.variables = {}
        self.functions = {
            "sin":1,
            "cos":1,
            "tan":1,
            "arcsin":1,
            "arccos":1,
            "arctan":1,
            "log":1,
            "ln":1,
            "sqrt":1,
            "abs":1,
            "exp":1,
            "pow":2,
        }
        self.functions["shape"]=1
        self.functions["det"]=1
        self.functions["trans"]=1
        self.functions["inv"]=1
        self.functions["identity"]=1
        self.functions["zeroes"]=2
        self.functions["integrate"]=2
        self.functions["diff"]=2
        self.functions["limit"]=3
        self.functions["solve"]=2
        self.functions["summation"]=3

    def define_variable(self, name: str):
        self.variables[name] = True

    def is_variable_defined(self, name: str) -> bool:
        return name in self.variables

    def is_function_defined(self, name: str) -> bool:
        return name in self.functions

    def function_arity(self, name: str) -> int:
        return self.functions[name] if name in self.functions else None
