class Token:
    def __init__(self, lox_type, lexeme, literal, line):
        self.type = lox_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
