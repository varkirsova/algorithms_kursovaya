class TokenizerError(Exception): #ошибка токенизации
    pass

class ParserError(Exception): #ошибка синтакс. анализа
    pass

class EvaluationError(Exception): #ошибка вычисления выражения
    pass

class InvalidCharacterError(TokenizerError): #в строке некорр. символ
    def __init__(self, char, position):
        super().__init__(f"некорректный символ '{char}' на позиции {position}")
        self.char = char
        self.position = position

class ParenthesisError(ParserError): #косяк в скобках
    def __init__(self, message):
        super().__init__(f"ошибка скобок: {message}")

class DivisionByZeroError(EvaluationError): #деление на ноль
    def __init__(self):
        super().__init__("деление на ноль")

class SyntaxError(ParserError): #синтакс. ошибка в выражении
    def __init__(self, message, position=None):
        if position is not None:
            super().__init__(f"синтаксическая ошибка на позиции {position}: {message}")
        else:
            super().__init__(f"синтаксическая ошибка: {message}")