from core.node import Node, NodeType
from utils.errors import *

class Evaluator:
    @staticmethod
    def evaluate(node: Node) -> float:
        try:
            return Evaluator._evaluate_node(node)
        except ZeroDivisionError as e:
            raise EvaluationError(f"деление на ноль в выражении")
        except (ValueError, TypeError) as e:
            raise EvaluationError(f"ошибка вычисления: {e}")

    @staticmethod
    def _evaluate_node(node: Node) -> float:

        # база: узел-число
        if node.type == NodeType.NUMBER:
            try:
                return float(node.value)
            except ValueError:
                raise EvaluationError(f"некорректное числовое значение: {node.value}")

        # унарный оператора (минус)
        elif node.type == NodeType.UNARY_OPERATOR:
            if node.value == '-':
                right_value = Evaluator._evaluate_node(node.right)
                return -right_value
            else:
                raise EvaluationError(f"неизвестный унарный оператор: {node.value}")

        # бинарные операторы
        elif node.type == NodeType.BINARY_OPERATOR:
            left_value = Evaluator._evaluate_node(node.left)
            right_value = Evaluator._evaluate_node(node.right)

            operator = node.value

            if operator == '+':
                return left_value + right_value
            elif operator == '-':
                return left_value - right_value
            elif operator == '*':
                return left_value * right_value
            elif operator == '/':
                if right_value == 0:
                    raise ZeroDivisionError("деление на ноль")
                return left_value / right_value
            elif operator == '^':
                try:
                    return left_value ** right_value
                except (ValueError, OverflowError) as e:
                    raise EvaluationError(f"ошибка возведения в степень: {e}")
            else:
                raise EvaluationError(f"неизвестный бинарный оператор: {operator}")

        else:
            raise EvaluationError(f"неизвестный тип узла: {node.type}")

    @staticmethod
    def safe_evaluate(node: Node) -> float:
        try:
            return Evaluator.evaluate(node)
        except EvaluationError:
            return None