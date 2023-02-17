from .folder import Folder


class Portfolio(Folder):
    def __init__(self, name="Portfolio", target=None, children=None):
        super().__init__(
            name, parent=None, target=target, children=children, newline=False
        )
