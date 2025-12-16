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

        if node.left is None and node.right is None:
            return [label], width, width // 2

        # только правый ребенок
        if node.left is None:
            right, rw, rm = visualizer._display(node.right)

            first = label + " " * rm + "\\"
            second = " " * width + " " * rm + "\\"

            shifted = [" " * width + line for line in right]

            return [first, second] + shifted, width + rw, width // 2

        # только левый ребенок
        if node.right is None:
            left, lw, lm = visualizer._display(node.left)

            first = " " * lm + "/" + " " * (lw - lm - 1) + label
            second = " " * lm + "/" + " " * (lw - lm - 1 + width)

            shifted = [line + " " * width for line in left]

            return [first, second] + shifted, lw + width, lw + width // 2

        # оба потомка
        left, lw, lm = visualizer._display(node.left)
        right, rw, rm = visualizer._display(node.right)

        first = (
            " " * lm +
            "/" +
            " " * (lw - lm - 1 + width + rm) +
            "\\"
        )

        second = (
            " " * lm +
            "/" +
            " " * (lw - lm - 1 + width + rm) +
            "\\"
        )

        label_line = " " * lw + label + " " * rw

        # выравнивание высот
        max_h = max(len(left), len(right))
        left += [" " * lw] * (max_h - len(left))
        right += [" " * rw] * (max_h - len(right))

        merged = [
            l + " " * width + r
            for l, r in zip(left, right)
        ]

        return [label_line, first, second] + merged, lw + width + rw, lw + width // 2
