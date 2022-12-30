class Metadata:
    def __init__(self, name: str, index: int, binary: bool, pointer: int, size: int = 0) -> None:
        self.__name = name
        self.__binary = binary
        self.__head = Block(index, pointer)
        self.size = size

    def add_block(self, index: int, pointer: int):
        node = self.__head
        while node.next is not None:
            node = node.next
        node.next = Block(index, pointer)

    @property
    def name(self) -> str: return self.__name
    @property
    def binary(self) -> bool: return self.__binary
    @property
    def head(self) -> 'Block': return self.__head
        

class Block:
    def __init__(self, index: int = 0, pointer: int = 0) -> None:
        self.next = None
        self.pointer = pointer
        self.index = index