from core.node import NodeType

class visualizer:
    @staticmethod
    def visualize(node, indent=4):
        lines, _, _ = visualizer._display(node, spacing=2)  # увеличен spacing для лучшего разделения
        for line in lines:
            print(" " * indent + line)

    @staticmethod
    def _display(node, spacing=2):
        """spacing - минимальное расстояние между поддеревьями"""
        label = str(node.value)
        width = len(label)

        # ===== ЧИСЛО =====
        if node.type == NodeType.NUMBER:
            return [label], width, width // 2

        # ===== УНАРНЫЙ ОПЕРАТОР =====
        if node.type == NodeType.UNARY_OPERATOR:
            # визуализируем правого потомка
            child_lines, cw, cm = visualizer._display(node.right, spacing)

            # Важно: оператор должен быть центрирован над ребенком
            child_mid = cm  # середина ребенка

            # Создаем линии для унарного оператора
            if child_mid >= 0:
                # Оператор над серединой ребенка
                first = " " * child_mid + label + " " * (cw - child_mid - 1)
                # Линия от оператора к ребенку
                second = " " * child_mid + "\\" + " " * (cw - child_mid - 1)
            else:
                # Если середина отрицательная (бывает в некоторых случаях)
                first = label + " " * (cw - 1)
                second = "\\" + " " * (cw - 1)

            # Ребенок без дополнительного сдвига
            shifted_child = child_lines

            return [first, second] + shifted_child, cw, max(0, child_mid)

        # ===== БИНАРНЫЙ ОПЕРАТОР =====
        left_lines, lw, lm = visualizer._display(node.left, spacing)
        right_lines, rw, rm = visualizer._display(node.right, spacing)

        # Добавляем spacing между поддеревьями
        space_between = max(spacing, 3)  # минимум 3 пробела между поддеревьями

        # Общая ширина
        total_width = lw + space_between + rw

        # Центр оператора
        operator_pos = lw + (total_width - lw - rw) // 2

        # Линия с оператором
        label_line = (
                " " * (operator_pos - width // 2) +
                label +
                " " * (total_width - operator_pos - width // 2)
        )

        # Ветки
        branch_left = " " * (operator_pos - 1) + "/"
        branch_right = " " * (total_width - operator_pos - 1) + "\\"

        # Объединяем ветки
        branch_line = list(" " * total_width)
        if operator_pos > 0:
            branch_line[operator_pos - 1] = "/"
        if operator_pos < total_width - 1:
            branch_line[operator_pos + 1] = "\\"
        branch_line = "".join(branch_line)

        # Выравниваем высоту поддеревьев
        max_h = max(len(left_lines), len(right_lines))
        left_lines += [" " * lw] * (max_h - len(left_lines))
        right_lines += [" " * rw] * (max_h - len(right_lines))

        # Соединяем поддеревья
        merged = [
            l + " " * space_between + r
            for l, r in zip(left_lines, right_lines)
        ]

        return [label_line, branch_line] + merged, total_width, operator_pos