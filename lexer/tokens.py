class Token():
    def __init__(self,type_, value=None,line=1, column=1):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type.name}, {self.value}, line={self.line}, column={self.column})'

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (
            self.type == other.type and
            self.value == other.value and
            self.line == other.line and
            self.column == other.column
        )

    def __ne__(self, other):
        return not self.__eq__(other)
