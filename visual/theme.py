from visual.color import Color


class Theme:

    def __init__(self, light_bg, dark_bg,
                 light_moves, dark_moves,
                 light_trace, dark_trace):

        self.chess_board = Color(light_bg, dark_bg)
        self.moves = Color(light_moves, dark_moves)
        self.trace = Color(light_trace, dark_trace)

