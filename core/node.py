class NodeType:
    NUMBER = 'number'

class Node:
    """атрибуты будут или нет?"""
    def __init__(self, value, node_type):
        self.value = value
        self.type = node_type
        self.left = None
        self.right = None

        self._validation()

    def _validation(self):
        #у числа не дб потомков;
        # у бин. опер. дб два потомка;
        #
        if self.node_type == NodeType.NUMBER:
            if self.left is not None or self.right is not None:
                raise ErrorValue("узел-число не должен иметь потомков!")
            if not isinstate(self.value, (int, float)):
                try:
                    self.value = int(self.value)
                except:
                    raise ErrorValue("некорректное числовое значение!")