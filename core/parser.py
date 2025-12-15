from node import Node, NodeType
from tokenizer import Tokenizer


class Parser:
    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer or Tokenizer()
        self.operators = {
            '+': 1, '-': 1,
            '*': 2, '/': 2,
            '^': 3,
            'u-': 4
        }

    def parse(self, expression):
        self.tokenizer.tokenize(expression)
        tree = self.parse_expression()

        if self.tokenizer.peek_token() is not None:
            remaining = []
            while self.tokenizer.peek_token() is not None:
                remaining.append(self.tokenizer.next_token())
            raise ValueError(f"Лишние токены: {remaining}")

        return tree

    def parse_primary(self):
        token = self.tokenizer.next_token()

        if token is None:
            raise ValueError("Неожиданный конец выражения")

        if token.isdigit():
            return Node(int(token), NodeType.NUMBER)

        elif token == 'u-':
            if self.tokenizer.peek_token() is None:
                raise ValueError("Ожидался операнд после унарного минуса")

            operand = self.parse_expression(min_precedence=1)
            return Node('-', NodeType.UNARY_OPERATOR, right=operand)

        elif token == '(':
            if self.tokenizer.peek_token() == ')':
                raise ValueError("Пустые скобки")

            expr = self.parse_expression()

            next_token = self.tokenizer.next_token()
            if next_token != ')':
                raise ValueError(f"Ожидалась ')', получено '{next_token}'")

            return expr

        else:
            raise ValueError(f"Неожиданный токен: '{token}'")

    def parse_expression(self, min_precedence=0):
        left = self.parse_primary()

        while True:
            token = self.tokenizer.peek_token()

            if (token is None or
                    token not in self.operators or
                    token == ')' or
                    self.operators[token] < min_precedence):
                break

            op_token = self.tokenizer.next_token()
            op_precedence = self.operators[op_token]

            if op_token != '^':
                next_min_precedence = op_precedence + 1
            else:
                next_min_precedence = op_precedence

            right = self.parse_expression(next_min_precedence)
            left = Node(op_token, NodeType.BINARY_OPERATOR, left, right)

        return left