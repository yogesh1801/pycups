import cups


class _Base:
    def __init__(self):
        self.cups = cups.Connection()
