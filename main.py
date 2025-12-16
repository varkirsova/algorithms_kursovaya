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
    print("=" * 70)
    print("ИНТЕРАКТИВНЫЙ КАЛЬКУЛЯТОР С AST")
    print("Операции: +  -  *  /  ^  ( )")
    print("Унарный минус поддерживается")
    print("Для выхода введите: exit")
    print("=" * 70)

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

            # --- ТОКЕНИЗАЦИЯ ---
            tokenizer.tokenize(expr)
            tokenizer.print_tokens()

            # --- ПАРСИНГ ---
            tree = parser.parse(expr)

            # --- AST ---
            print("\nAST (визуализация):")
            visualizer.visualize(tree)

            # --- НОТАЦИИ ---
            print("\nНотации:")
            print("  Infix   :", tree.infix())
            print("  Prefix  :", tree.prefix())
            print("  Postfix :", tree.postfix())

            # --- ВЫЧИСЛЕНИЕ ---
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
