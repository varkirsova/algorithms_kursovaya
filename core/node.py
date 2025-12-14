class NodeType:
    NUMBER = 'number'
    BINARY_OPERATOR = 'binary_operator'
    UNARY_OPERATOR = 'unary_operator'

class Node:
    """атрибуты будут или нет?"""
    def __init__(self, value, node_type, left=None, right=None):
        self.value = value
        self.type = node_type
        self.left = left
        self.right = right

        self._validate()

    def _validate(self):
        #у числа не дб потомков;
        # у бин. опер. дб два потомка;
        # у ун. опер. дм иметь одного потомка (правого)
        if self.type == NodeType.NUMBER:
            if self.left is not None or self.right is not None:
                raise ValueError("узел-число не должен иметь потомков!")
            if not isinstance(self.value, (int, float)):
                try:
                    self.value = int(self.value)
                except:
                    raise ValueError("некорректное числовое значение!")

        elif self.type == NodeType.BINARY_OPERATOR:
            if self.left is None or self.right is None:
                raise ValueError("бинарный оператор должен иметь двух потомков!")
            if self.value not in ['+', '-', '*', '/']:
                raise ValueError(f"неподходящий оператор: {self.value}")

        elif self.type == NodeType.UNARY_OPERATOR:
            if self.right is None:
                raise ValueError("унарный оператор должен иметь одного потомка!")
            if self.left is not None:
                raise ValueError("унарный оператор должен иметь только правого потомка!")
            if self.value != '-':
                raise ValueError(f"неподходящий унарный оператор: {self.value}")

    def is_leaf(self):
        return self.type == NodeType.NUMBER
    def is_operator(self):
        return self.type in [NodeType.BINARY_OPERATOR, NodeType.UNARY_OPERATOR]
    def __str__(self):
        if self.type == NodeType.NUMBER:
            return f"Number({self.value})"

        elif self.type == NodeType.BINARY_OPERATOR:
            left_str = str(self.left.value) if self.left is not None else "None"
            right_str = str(self.right.value) if self.right is not None else "None"

            return f"BinOp({self.value}, L={left_str}, R={right_str})"

        elif self.type == NodeType.UNARY_OPERATOR:
            right_str = str(self.right.value) if self.right is not None else "None"

            return f"UnOp({self.value}, R={right_str})"
    def __repr__(self):
        return self.__str__()