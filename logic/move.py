
class Move:

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop
