import re #для регулярных выражений
from enum import Enum #перечисление типов токенов
class TokenType(Enum):
    NUMBER = 'NUMBER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'  # бинарный
    UNARY_MINUS = 'UNARY_MINUS'  # унарный
    MULTIPLY = 'MULTIPLY'  # *
    DIVIDE = 'DIVIDE'  # /
    POWER = 'POWER'  # ^
    LPAREN = 'LPAREN'  # (
    RPAREN = 'RPAREN'  # )
    EOF = 'EOF'  # конец выражения

class Token:
    def __init__(self, type_: TokenType, value: str, position: int = 0):
        self.type = type_
        self.value = value
        self.position = position

    def __str__(self):
        if self.type == TokenType.NUMBER:
            return f"число({self.value})"

        elif self.type == TokenType.PLUS:
            return f"сложение(+)"

        elif self.type == TokenType.MINUS:
            return f"вычитание(-)"

        elif self.type == TokenType.UNARY_MINUS:
            return f"унарный минус(-)"

        elif self.type == TokenType.MULTIPLY:
            return f"умножение(*)"

        elif self.type == TokenType.DIVIDE:
            return f"деление(/)"

        elif self.type == TokenType.POWER:
            return f"степень(^)"

        elif self.type == TokenType.LPAREN:
            return f"левая скобка('(')"

        elif self.type == TokenType.RPAREN:
            return f"правая скобка(')')"

        elif self.type == TokenType.EOF:
            return f"конец выражения"

        else:
            return f"Token({self.type.name}, '{self.value}')"

    def __repr__(self):
        return self.__str__()

class TokenizerError(Exception):
    pass

class InvalidCharacterError(TokenizerError):
    def __init__(self, char, position):
        super().__init__(f"некорректный символ '{char}' на позиции {position}")
        self.char = char
        self.position = position

class Tokenizer: #строка -> список токенов
    TOKEN_PATTERNS = [
        (r'\d+', TokenType.NUMBER), # >=1 цифр
        (r'\+', TokenType.PLUS),
        (r'-', TokenType.MINUS),
        (r'\*', TokenType.MULTIPLY),
        (r'/', TokenType.DIVIDE),
        (r'\^', TokenType.POWER),
        (r'\(', TokenType.LPAREN),
        (r'\)', TokenType.RPAREN),
    ]

    def __init__(self):
        self.tokens = []
        self.current_pos = 0
        self.expression = "" #исх. выражение
        self.compiled_patterns = None #скомпил. регуляр. выражения, типа кэщ

    def tokenize(self, expression: str) -> list[Token]:
        self.expression = expression
        self.current_pos = 0
        self.tokens = []

        expression_without_spaces = expression.replace(' ', '')
        if not expression_without_spaces:
            self.tokens.append(Token(TokenType.EOF, '', 0))
            return self.tokens

        if self.compiled_patterns is None:
            self.compiled_patterns = []

            for pattern, token_type in self.TOKEN_PATTERNS:
                self.compiled_patterns.append((re.compile('^'+pattern), token_type))

        while expression:
            matched = False
            for pattern, token_type in self.compiled_patterns:
                match = pattern.match(expression)

                if match:
                    value = match.group(0)

                    token = Token(token_type, value, self.current_pos)
                    self.tokens.append(token)
                    self.current_pos += len(value)
                    expression = expression[len(value):]
                    matched = True
                    break

            if not matched:
                raise InvalidCharacterError(expression[0], self.current_pos)

        self._identify_minus_types()

        self.tokens.append(Token(TokenType.EOF, '', self.current_pos))

        return self.tokens

    def _identify_minus_types(self):
        for i, token in enumerate(self.tokens):
            if token.type == TokenType.MINUS:
                if self._is_unary_minus(i):
                    token.type = TokenType.UNARY_MINUS

    def _is_unary_minus(self, position: int) -> bool:
        if position == 0:
            return True

        prev_token = self.tokens[position - 1]

        # унарный, если перед ним ( или оператор
        unary_triggers = [
            TokenType.PLUS, TokenType.MINUS, TokenType.UNARY_MINUS,
            TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.POWER,
            TokenType.LPAREN
        ]

        return prev_token.type in unary_triggers

    def get_token_value(self, token):
        if token.type == TokenType.EOF:
            return None

        if token.type == TokenType.UNARY_MINUS:
            return "u-"
        elif token.type == TokenType.MINUS:
            return "-"
        elif token.type == TokenType.PLUS:
            return "+"
        elif token.type == TokenType.MULTIPLY:
            return "*"
        elif token.type == TokenType.DIVIDE:
            return "/"
        elif token.type == TokenType.POWER:
            return "^"
        elif token.type == TokenType.LPAREN:
            return "("
        elif token.type == TokenType.RPAREN:
            return ")"
        elif token.type == TokenType.NUMBER:
            return token.value
        else:
            return token.value
    def next_token(self):
        if self.current_pos < len(self.tokens):
            token = self.tokens[self.current_pos]
            self.current_pos += 1
            return self.get_token_value(token)
        return None

    def peek_token(self):
        if self.current_pos < len(self.tokens):
            token = self.tokens[self.current_pos]
            return self.get_token_value(token)



    def print_tokens(self):
        print("Список токенов:")
        for token in self.tokens:
            print(f"  {token}")