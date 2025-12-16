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
        """Основной метод парсинга"""
        self.tokenizer.tokenize(expression)
        self.tokenizer.current_pos = 0

        tree = self._parse_expression()

        # Проверяем, что все токены обработаны
        next_token = self.tokenizer.next_token()
        if next_token is not None:
            raise ValueError(f"Лишние токены после выражения: '{next_token}'")

        return tree

    def _parse_expression(self, min_precedence=0):
        """Парсит выражение с учетом приоритетов"""
        # Обработка унарного минуса
        if self.tokenizer.peek_token() == 'u-':
            self.tokenizer.next_token()  # забираем 'u-'
            operand = self._parse_expression(min_precedence=5)  # унарный минус имеет приоритет 5
            left = Node('-', NodeType.UNARY_OPERATOR, right=operand)
        else:
            # Иначе парсим обычный primary
            left = self._parse_primary()

        # Парсим бинарные операторы
        while True:
            token = self.tokenizer.peek_token()

            # Условия выхода
            if (token is None or
                    token not in self.operators or
                    token == ')' or
                    self.operators.get(token, 0) < min_precedence):
                break

            op_token = self.tokenizer.next_token()
            op_precedence = self.operators[op_token]

            # Для степени - правоассоциативность
            if op_token == '^':
                next_min_precedence = op_precedence
            else:
                next_min_precedence = op_precedence + 1

            # Парсим правую часть
            right = self._parse_expression(next_min_precedence)

            # Создаем узел
            left = Node(op_token, NodeType.BINARY_OPERATOR, left, right)

        return left

    def _parse_primary(self):
        """Парсит числа и выражения в скобках"""
        token = self.tokenizer.next_token()

        if token is None:
            raise ValueError("Неожиданный конец выражения")

        # Число
        if token and self._is_number(token):
            return Node(int(token), NodeType.NUMBER)

        # Скобки
        elif token == '(':
            expr = self._parse_expression()
            next_token = self.tokenizer.next_token()
            if next_token != ')':
                raise ValueError(f"Ожидалась ')', получено '{next_token}'")
            return expr

        else:
            raise ValueError(f"Неожиданный токен: '{token}'")

    def _is_number(self, token):
        """Проверяет, является ли токен числом"""
        if not token:
            return False

        # Убираем возможный минус в начале
        if token[0] == '-':
            return token[1:].isdigit()
        return token.isdigit()