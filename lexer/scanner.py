from errors.error import error
from lexer.lox_token import Token
from lexer.lox_token_type import TokenType


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []
        self.had_error = False

    def add_non_literal_token(self, token_type: TokenType) -> None:
        self.add_token(token_type, "")

    def add_slash_token(self) -> None:
        if self.match("/"):
            self.ignore_comment()
        else:
            self.add_non_literal_token(TokenType.SLASH)

    def add_token(self, token_type: TokenType, literal: str) -> None:
        self.tokens.append(
            Token(token_type, self.get_current_lexeme(), literal, self.line)
        )

    def advance(self) -> str:
        self.current += 1
        self.column += 1
        return self.source[self.current - 1]

    def get_current_lexeme(self) -> str:
        return self.source[self.start : self.current]

    def handle_identifier(self) -> None:
        keywords = [
            TokenType.AND,
            TokenType.CLASS,
            TokenType.ELSE,
            TokenType.FALSE,
            TokenType.FUN,
            TokenType.FOR,
            TokenType.IF,
            TokenType.NIL,
            TokenType.OR,
            TokenType.PRINT,
            TokenType.RETURN,
            TokenType.SUPER,
            TokenType.THIS,
            TokenType.TRUE,
            TokenType.VAR,
            TokenType.WHILE,
        ]
        while self.peek().isalnum():
            self.advance()
        text = self.get_current_lexeme()
        if text in keywords:
            self.add_non_literal_token(text)
        else:
            self.add_token(TokenType.IDENTIFIER, text)

    def handle_number(self) -> None:
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, self.get_current_lexeme())

    def handle_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            error(self.line, "Unterminated string.")
            self.had_error = True
            return
        self.advance()
        literal = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, literal)

    def ignore_comment(self) -> None:
        while self.peek() != "\n" and not self.is_at_end():
            self.advance()

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.peek() != expected:
            return False
        self.advance()  # advances a second time for two-char token
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def scan_token(self) -> None:
        c = self.advance()
        if c == "(":
            self.add_non_literal_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_non_literal_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_non_literal_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_non_literal_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_non_literal_token(TokenType.COMMA)
        elif c == ".":
            self.add_non_literal_token(TokenType.DOT)
        elif c == "-":
            self.add_non_literal_token(TokenType.MINUS)
        elif c == "+":
            self.add_non_literal_token(TokenType.PLUS)
        elif c == ";":
            self.add_non_literal_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_non_literal_token(TokenType.STAR)
        elif c == "!":
            self.add_non_literal_token(
                TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
            )
        elif c == "=":
            self.add_non_literal_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            )
        elif c == "<":
            self.add_non_literal_token(
                TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
            )
        elif c == ">":
            self.add_non_literal_token(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            )
        elif c == "/":
            self.add_slash_token()
        elif c in [" ", "\r", "\t"]:
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.handle_string()
        elif c.isdigit():
            self.handle_number()
        elif c.isalpha():
            self.handle_identifier()
        else:
            error(self.line, f"Unexpected character '{c}'.")
            self.had_error = True

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        if not self.had_error:
            self.add_non_literal_token(TokenType.EOF)
        return self.tokens
