from core.node import Node, NodeType
from core.tokenizer import Tokenizer


class Parser:
    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer or Tokenizer()
        self.operators = {
            '+': 1, '-': 1,
            '*': 2, '/': 2,
            '^': 3,
            'u-': 5  # унарный минус имеет высший приоритет
        }

    def parse(self, expression):
        self.tokenizer.tokenize(expression)
        self.tokenizer.current_pos = 0

        tree = self._parse_expression()

        # все ли токены обработаны
        next_token = self.tokenizer.next_token()
        if next_token is not None:
            raise ValueError(f"Лишние токены после выражения: '{next_token}'")

        return tree

    def _parse_expression(self, min_precedence=0):
        if self.tokenizer.peek_token() == 'u-':
            self.tokenizer.next_token()
            operand = self._parse_expression(min_precedence=5)
            left = Node('-', NodeType.UNARY_OPERATOR, right=operand)
        else:
            left = self._parse_primary()

        # бинарные операторы
        while True:
            token = self.tokenizer.peek_token()

            if (token is None or
                    token not in self.operators or
                    token == ')' or
                    self.operators.get(token, 0) < min_precedence):
                break

            op_token = self.tokenizer.next_token()
            op_precedence = self.operators[op_token]

            # Для ^ правоассоциативность
            if op_token == '^':
                next_min_precedence = op_precedence
            else:
                next_min_precedence = op_precedence + 1

            right = self._parse_expression(next_min_precedence)
            left = Node(op_token, NodeType.BINARY_OPERATOR, left, right)

        return left

    def _parse_primary(self):
        token = self.tokenizer.next_token()

        if token is None:
            raise ValueError("Неожиданный конец выражения")

        # число
        if token and self._is_number(token):
            return Node(int(token), NodeType.NUMBER)

        # скобки
        elif token == '(':
            expr = self._parse_expression()
            next_token = self.tokenizer.next_token()
            if next_token != ')':
                raise ValueError(f"Ожидалась ')', получено '{next_token}'")
            return expr

        else:
            raise ValueError(f"Неожиданный токен: '{token}'")

    def _is_number(self, token):
        if not token:
            return False

        if token[0] == '-':
            return token[1:].isdigit()
        return token.isdigit()