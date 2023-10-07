from typing import Protocol


class Page(Protocol):
    def process(self):
        raise NotImplementedError
