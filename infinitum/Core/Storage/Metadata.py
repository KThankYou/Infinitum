class Metadata:
    def __init__(self, name: str, index: int, pointer: int, size: int = 0, app: bool = False) -> None:
        self.name = name
        self.head = Block(index, pointer)
        self.size = size
        self.app = app

    def add_block(self, index: int, pointer: int):
        node = self.head
        while node.next is not None:
            node = node.next
        node.next = Block(index, pointer)
    
    def __repr__(self) -> str:
        return f'Metadata({self.name}, {self.size}, {self.head})'


class Block:
    def __init__(self, index: int = 0, pointer: int = 0) -> None:
        self.next = None
        self.pointer = pointer
        self.index = index

    def __str__(self) -> str:
        return f'{repr(self)} -> {self.next}'

    def __repr__(self) -> str:
        return f'Block({self.index}, {self.pointer})'