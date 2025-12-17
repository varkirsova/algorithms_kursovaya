from core.node import NodeType

class visualizer:
    @staticmethod
    def visualize(node, indent=4):
        lines, _, _ = visualizer._display(node, spacing=2)
        for line in lines:
            print(" " * indent + line)

    @staticmethod
    def _display(node, spacing=2):
        label = str(node.value)
        width = len(label)

        if node.type == NodeType.NUMBER:
            return [label], width, width // 2

        if node.type == NodeType.UNARY_OPERATOR:
            # визуализируем правого ребенка
            child_lines, cw, cm = visualizer._display(node.right, spacing)

            child_mid = cm  # середина ребенка

            if child_mid >= 0:
                first = " " * child_mid + label + " " * (cw - child_mid - 1)
                second = " " * child_mid + "\\" + " " * (cw - child_mid - 1)
            else:
                first = label + " " * (cw - 1)
                second = "\\" + " " * (cw - 1)

            shifted_child = child_lines

            return [first, second] + shifted_child, cw, max(0, child_mid)

        left_lines, lw, lm = visualizer._display(node.left, spacing)
        right_lines, rw, rm = visualizer._display(node.right, spacing)

        space_between = max(spacing, 3)
        total_width = lw + space_between + rw
        operator_pos = lw + (total_width - lw - rw) // 2

        label_line = (
                " " * (operator_pos - width // 2) +
                label +
                " " * (total_width - operator_pos - width // 2)
        )

        branch_line = list(" " * total_width)
        if operator_pos > 0:
            branch_line[operator_pos - 1] = "/"
        if operator_pos < total_width - 1:
            branch_line[operator_pos + 1] = "\\"
        branch_line = "".join(branch_line)

        max_h = max(len(left_lines), len(right_lines))
        left_lines += [" " * lw] * (max_h - len(left_lines))
        right_lines += [" " * rw] * (max_h - len(right_lines))

        merged = [
            l + " " * space_between + r
            for l, r in zip(left_lines, right_lines)
        ]

        return [label_line, branch_line] + merged, total_width, operator_pos
