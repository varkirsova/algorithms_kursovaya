from core.node import NodeType

class visualizer:
    @staticmethod
    def visualize(node):
        lines, _, _ = visualizer._display(node)
        for line in lines:
            print(line)

    @staticmethod
    def _display(node):
        label = str(node.value)
        width = len(label)

        # ===== ЧИСЛО =====
        if node.type == NodeType.NUMBER:
            return [label], width, width // 2

        # ===== УНАРНЫЙ ОПЕРАТОР =====
        if node.type == NodeType.UNARY_OPERATOR:
            # визуализируем правого потомка
            child_lines, cw, cm = visualizer._display(node.right)

            # оператор слева от child (линия от родителя через /)
            first = label + " " * (cw - 1)  # сдвиг под ребенка
            second = "\\" + " " * (cw - 1)  # линия к child

            # сдвигаем потомка вправо под линию
            shifted_child = [" " + line for line in child_lines]

            return [first, second] + shifted_child, cw, 0  # mid=0 чтобы родитель соединялся слева

        # ===== БИНАРНЫЙ ОПЕРАТОР =====
        left_lines, lw, lm = visualizer._display(node.left)
        right_lines, rw, rm = visualizer._display(node.right)

        label_line = " " * lw + label + " " * rw

        branch = (
            " " * lm +
            "/" +
            " " * (lw - lm - 1 + width + rm) +
            "\\"
        )

        # выравниваем высоту поддеревьев
        max_h = max(len(left_lines), len(right_lines))
        left_lines += [" " * lw] * (max_h - len(left_lines))
        right_lines += [" " * rw] * (max_h - len(right_lines))

        merged = [
            l + " " * width + r
            for l, r in zip(left_lines, right_lines)
        ]

        return [label_line, branch] + merged, lw + width + rw, lw + width // 2