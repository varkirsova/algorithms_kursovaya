# from core.node import NodeType
#
# class visualizer:
#     @staticmethod
#     def visualize(node, indent=4):
#         lines, _, _ = visualizer._display(node, spacing=2)
#         for line in lines:
#             print(" " * indent + line)
#
#     @staticmethod
#     def _display(node, spacing=2):
#         label = str(node.value)
#         width = len(label)
#
#         if node.type == NodeType.NUMBER:
#             return [label], width, width // 2
#
#         if node.type == NodeType.UNARY_OPERATOR:
#             # визуализируем правого ребенка
#             child_lines, cw, cm = visualizer._display(node.right, spacing)
#
#             child_mid = cm  # середина ребенка
#
#             if child_mid >= 0:
#                 first = " " * child_mid + label + " " * (cw - child_mid - 1)
#                 second = " " * child_mid + "\\" + " " * (cw - child_mid - 1)
#             else:
#                 first = label + " " * (cw - 1)
#                 second = "\\" + " " * (cw - 1)
#
#             shifted_child = child_lines
#
#             return [first, second] + shifted_child, cw, max(0, child_mid)
#
#         left_lines, lw, lm = visualizer._display(node.left, spacing)
#         right_lines, rw, rm = visualizer._display(node.right, spacing)
#
#         space_between = max(spacing, 3)
#         total_width = lw + space_between + rw
#         operator_pos = lw + (total_width - lw - rw) // 2
#
#         label_line = (
#                 " " * (operator_pos - width // 2) +
#                 label +
#                 " " * (total_width - operator_pos - width // 2)
#         )
#
#         branch_line = list(" " * total_width)
#         if operator_pos > 0:
#             branch_line[operator_pos - 1] = "/"
#         if operator_pos < total_width - 1:
#             branch_line[operator_pos + 1] = "\\"
#         branch_line = "".join(branch_line)
#
#         max_h = max(len(left_lines), len(right_lines))
#         left_lines += [" " * lw] * (max_h - len(left_lines))
#         right_lines += [" " * rw] * (max_h - len(right_lines))
#
#         merged = [
#             l + " " * space_between + r
#             for l, r in zip(left_lines, right_lines)
#         ]
#
#         return [label_line, branch_line] + merged, total_width, operator_pos


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

        if node.type == NodeType.NUMBER:
            return [label], width, width // 2

        if node.type == NodeType.UNARY_OPERATOR:
            child_lines, cw, cm = visualizer._display(node.right)

            # Унарный оператор
            if cm >= 0:
                first = " " * cm + label + " " * (cw - cm - 1)
                second = " " * cm + "\\" + " " * (cw - cm - 1)
            else:
                first = label + " " * (cw - 1)
                second = "\\" + " " * (cw - 1)

            return [first, second] + child_lines, cw, 0

        # БИНАРНЫЙ ОПЕРАТОР
        left_lines, lw, lm = visualizer._display(node.left)
        right_lines, rw, rm = visualizer._display(node.right)

        # Отступ между поддеревьями
        spacing = 2
        total_width = lw + spacing + rw

        # Оператор посередине между центрами поддеревьев
        left_center = lm
        right_center = lw + spacing + rm
        operator_pos = (left_center + right_center) // 2

        # Строка с оператором
        label_start = operator_pos - width // 2
        label_line = list(" " * total_width)
        for i in range(width):
            pos = label_start + i
            if 0 <= pos < total_width:
                label_line[pos] = label[i]
        label_line = "".join(label_line)

        # Ветки
        branch_line = list(" " * total_width)

        # Левая ветка
        if lw > 0 and lm >= 0 and lm < len(branch_line):
            if operator_pos > lm:
                branch_line[lm] = "/"

        # Правая ветка
        right_branch_pos = lw + spacing + rm
        if rw > 0 and rm >= 0 and right_branch_pos < len(branch_line):
            if operator_pos < right_branch_pos:
                branch_line[right_branch_pos] = "\\"

        branch_line = "".join(branch_line)

        # Объединяем поддеревья
        max_h = max(len(left_lines), len(right_lines))
        left_lines += [" " * lw] * (max_h - len(left_lines))
        right_lines += [" " * rw] * (max_h - len(right_lines))

        merged = []
        for i in range(max_h):
            merged.append(left_lines[i] + " " * spacing + right_lines[i])

        return [label_line, branch_line] + merged, total_width, operator_pos