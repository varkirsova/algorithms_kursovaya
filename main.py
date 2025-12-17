from core.tokenizer import Tokenizer
from core.parser import Parser
from core.evaluator import Evaluator
from utils.visualizer import visualizer

from utils.errors import (
    TokenizerError,
    ParserError,
    EvaluationError
)

def main():
    print("Дерево выражений.")
    print("Операции: +  -  *  /  ^  ( )")
    print("Унарный минус поддерживается")
    print("Для выхода введите: exit")

    tokenizer = Tokenizer()
    parser = Parser(tokenizer)

    while True:
        try:
            expr = input("\nВведите выражение >>> ").strip()

            if expr.lower() in ("exit", "quit"):
                print("Выход.")
                break

            if not expr:
                print("Пустая строка.")
                continue

            tokenizer.tokenize(expr)
            tokenizer.print_tokens()

            tree = parser.parse(expr)

            print("\nВизуализация:")
            visualizer.visualize(tree)

            print("\nФормы записи:")
            print("  Infix   :", tree.infix())
            print("  Prefix  :", tree.prefix())
            print("  Postfix :", tree.postfix())

            result = Evaluator.evaluate(tree)
            print("\nРезультат:")
            print(" ", result)

        except TokenizerError as e:
            print("\n[Ошибка токенизации]")
            print(" ", e)

        except ParserError as e:
            print("\n[Ошибка синтаксиса]")
            print(" ", e)

        except EvaluationError as e:
            print("\n[Ошибка вычисления]")
            print(" ", e)

        except Exception as e:
            print("\n[Неизвестная ошибка]")
            print(" ", e)


if __name__ == "__main__":
    main()
