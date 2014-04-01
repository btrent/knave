
class GameState:
    Inactive = 0
    Active = 1
    Observe = 2
    Examine = 3
    Setup = 4

class Varient:
    Classical = 0
    Bughouse = 1
    Crazyhouse = 2
    Atomic = 3
    Suicide = 4
    Losers = 5
    Chess960 = 6

class Game:
    WHITE = 0
    BLACK = 1

    state = GameState.Inactive
    is_droppable = 0 # is this a droppable game, like bughouse?
    is_960 = 0
    clock_tick = -1 # -1 = none, 0 = black, 1 = white
    white_castle = [True, True] # short and long
    black_castle = [True, True]
    board = None
    board_widget = None
    color_to_move = WHITE
    ep_square = None
    fifty_count = 0 # half moves since last irreversible move, for 50 move draws
    repeat_count = 0 # for 3 move repetition
    last_move = None
    move_list = []
    result = None
    varient = Varient.Classical
    zobrist = None # hopeful thinking for one day implementing
    is_check = False # true if a king is in check

    def __init__(self, *args, **keywords):
        pass

    def make_fics_move(style12):
        print style12

    def move(move):
        pass

    def all_legal_moves():
        return board.all_legal_moves()

class ClassicalGame(Game):
    def __init__(self, widget, **keywords):
        board_widget = widget
        board = widget.board

        print board.all_legal_moves()

