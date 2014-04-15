from threading import Thread, RLock
import traceback
import datetime
import os
import sys
import random

sys.platform = 'linux2'
    
import kivy
from kivy.config import Config, ConfigParser

from kivy_util import ScrollableLabel
from kivy_util import ScrollableGrid

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import Settings, SettingItem, SettingsPanel
from kivy.uix.screenmanager import SlideTransition

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty

from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.utils import get_color_from_hex
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.core.text.markup import MarkupLabel
from kivy.adapters.listadapter import ListAdapter

from kivy.uix.listview import ListItemButton, CompositeListItem, ListView
from kivy.uix.dropdown import DropDown
from kivy.uix.filechooser import FileChooserListView

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.properties import ListProperty

from chesstools import Board, Move
from sets import Set
import itertools as it
from operator import attrgetter
from time import sleep

from pychess.ic.FICSConnection import FICSConnection
from pychess.ic.managers.BoardManager import BoardManager

"""
from chess.game import Game
from chess.game_node import PIECE_FONT_MAP
from chess import PgnFile
from chess.game_node import GameNode
from chess.game_header_bag import GameHeaderBag
"""

THINKING_TIME = "[color=000000]Thinking..\n[size=24]{0}    [b]{1}[/size][/b][/color]"
THINKING = "[color=000000][b][size=16]Thinking..[/size][/b][/color]"

INDEX_TOTAL_GAME_COUNT = "total_game_count"


DELETE_FROM_USER_BOOK = "delete_from_user_book"

ADD_TO_USER_BOOK = "add_to_user_book"

REF_ = '[ref='

BOOK_POSITION_UPDATE = "BOOK_POSITION_UPDATE"

Clock.max_iteration = 20

GAME_HEADER = 'New Game'

ENGINE_PLAY = "engine_play"

ENGINE_PLAY_STOP = "play_stop"

ENGINE_PLAY_HINT = "play_hint"

YOURTURN_MENU = u"[color=000000][size=24][i]{2}[/i]    [b]{3}[/b][/size]\nYour turn\n[ref="+ENGINE_PLAY_STOP+"]Stop[/ref]\n\n[ref="+ENGINE_PLAY_HINT+"]Hint: {0}\nScore: {1} [/ref][/color]"

TRAIN_MENU = u"[color=000000][b]{0}    [/b]{1}[b]\n\n\n[ref="+ENGINE_PLAY_STOP+"]Stop[/ref][/b][/color]"

ENGINE_ANALYSIS = "engine_analysis"

ENGINE_TRAINING = "engine_training"

ENGINE_HEADER = '[b][color=000000][ref='+ENGINE_ANALYSIS\
                +']Analysis[/ref][ref='+ENGINE_PLAY+']\n\n' \
                'Play vs Comp [/ref][ref='+ENGINE_TRAINING+']\n\nTrain[/ref][/color][/b]'

MOVE_OUT_FORMAT = '[color=000000][b]{0}[/b][/color]'

BOOK_ON = "Book"
USER_BOOK_ON = "User Book"
SHOW_GAMES = "Show Games"
SHOW_REF_GAMES = "Show Reference Games"
BOOK_OFF = "Hide"

BOOK_HEADER = '[b][color=000000][ref=Book]{0}[/ref][/color][/b]'

DATABASE_HEADER = '[b][color=000000][ref=Database]{0}[/ref][/color][/b]'

DB_SORT_ASC = unichr(8710)
DB_SORT_DESC = 'V'


SQUARES = ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "a6",
              "b6", "c6", "d6", "e6", "f6", "g6", "h6", "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "a4", "b4",
              "c4", "d4", "e4", "f4", "g4", "h4", "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "a2", "b2", "c2",
              "d2", "e2", "f2", "g2", "h2", "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]

light_squares = Set([0,2,4,6,9,11,13,15,16,18,20,22,25,27,29,31,32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63])

IMAGE_PIECE_MAP = {
    "B": "wb",
    "R": "wr",
    "N": "wn",
    "Q": "wq",
    "K": "wk",
    "P": "wp",
    "b": "bb",
    "r": "br",
    "n": "bn",
    "q": "bq",
    "k": "bk",
    "p": "bp"
}

SPOKEN_PIECE_SOUNDS = {
    "B": " Bishop ",
    "N": " Knight ",
    "R": " Rook ",
    "Q": " Queen ",
    "K": " King ",
    "O-O": " Castles ",
    "++": " Double Check ",
}

img_piece_abv={"B":"WBishop", "R":"WRook", "N":"WKnight", "Q":"WQueen", "K":"WKing", "P": "WPawn",
"b":"BBishop", "r":"BRook", "n":"BKnight", "q":"BQueen", "k":"BKing", "p":"BPawn"}

COLOR_MAPS = {
    'black': get_color_from_hex('#000000'),
    'white': (0, 0, 0, 1),
    'wood': get_color_from_hex('#a68064'),
    #'cream': get_color_from_hex('#f9fcc6'),
    #'brown': get_color_from_hex('#969063'),
    'cream': get_color_from_hex('#f1ece7'),
    'brown': get_color_from_hex('#f2a257'),
    }

DARK_SQUARE = "img/board/dark/"
LIGHT_SQUARE = "img/board/light/"

MERIDA = "img/pieces/Merida-shadow/"

INITIAL_BOARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
INDEX_FILE_POS = "last_pos"

DB_HEADER_MAP = {"White": 0, "WhiteElo": 1, "Black": 2,
                 "BlackElo": 3, "Result": 4, "Date": 5, "Event": 6, "Site": 7,
                 "ECO": 8, INDEX_FILE_POS:9, "FEN":10}

arduino = False
try:
    import nanpy
    arduino = True
except ImportError:
    arduino = False

config = ConfigParser()

class KThread(Thread):
    """A subclass of threading.Thread, with a kill()
  method."""
    def __init__(self, *args, **keywords):
        Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run      # Force the Thread to install our trace.
        Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the
    trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

class ChessBoardWidget(Widget):
    _moving_piece_pos = ListProperty([0, 0])
    _moving_piece = '.'
    _moving_piece_from = -1
    _animate_from_origin = False
    _game = None

    def _update_after_animation(self, anim, *args):
        if hasattr(anim, 'fen'):
            self.set_position(anim.fen)
            self._draw_board()
            self._draw_pieces()
        elif hasattr(anim, 'move'):
            # print('ANIMMOVE : ' + anim.move)
            # self.fen = sf.get_fen(self._game.start_position, self._game.moves+[anim.move])
            # self._game.moves.append(anim.move)
            self.app.process_move(anim.move)
            self.update_position(anim.move)
#            self.set_position(self.app.chessboard.position)
            self.set_position(self.board.fen())
            self._draw_board()
            self._draw_pieces()
        else:
            self._moving_piece_from = -1
            self._moving_piece = '.'

    def update_position(self, move):
        """
        print "pos: "
        print self.app.chessboard.position
        print "move: "
        print move
        print "trying to make move: " + move[0:2] + "-" + move[2:4]
        print self.board
        """
        move_obj = Move(move[0:2],move[2:4])
        move_result = self.board.move(move_obj)

        if move_result is True:
            self.last_move_san = move_obj.pgn

        return True

    def set_position(self, fen):
        self.fen = self.board.fen()
        print self.fen
        self.position = fen.split(' ')[0].replace('/', '')
        for i in range(1, 9):
            self.position = self.position.replace(str(i), '.' * i)
        self._moving_piece_from = -1
        self._moving_piece = '.'

    def _to_square(self, touch):
        f = int((touch.x - self.bottom_left[0]) / self.square_size)
        r = 7 - int((touch.y - self.bottom_left[1]) / self.square_size)
        return -1 if (touch.x - self.bottom_left[0]) < 0 or f > 7 or (
            touch.y - self.bottom_left[1]) < 0 or r > 7 else f + r * 8

    def _to_coordinates(self, square):
        return (square % 8) * self.square_size + self.bottom_left[0], (7 - (square / 8)) * self.square_size + self.bottom_left[1]

    def _highlight_square_name(self, square_name):
        square = self.square_number(square_name)
        self._highlight_square(square)

    def _highlight_square(self, square):
        with self.canvas:
            Color(*self.highlight_color)
            left, bottom = self._to_coordinates(square)
            Line(points=[left, bottom, left + self.square_size, bottom, left + self.square_size, bottom + self.square_size,
                         left, bottom + self.square_size], width=2, close=True)

    def _draw_piece(self, piece, position):
        if piece != '.':
            with self.canvas:
                Color(*self.white)
                label = self.piece_textures[self._background_textures[piece]]
                Rectangle(texture=label.texture, pos=position, size=label.texture_size)
                Color(*self.black)
                label = self.piece_textures[self._front_textures[piece]]
                Rectangle(texture=label.texture, pos=position, size=label.texture_size)

    def _draw_pieces(self, skip=-1):
        i = 0
        for p in self.position:
            if p != '.' and i != skip:
                self._draw_piece(p, self._to_coordinates(i))
            i += 1

    def _draw_board(self):
        with self.canvas:
            self.canvas.clear()
            Color(*self.white)

            Rectangle(pos=self.bottom_left, texture=self.dark_img.texture, size=(self.board_size, self.board_size))
            # Color(*self.light)
            for row in range(8):
                for file in range(8):
                    if (row + file) & 0x1:
                        Rectangle(pos=(
                            self.bottom_left[0] + file * self.square_size, self.bottom_left[1] + row * self.square_size), texture=self.light_img.texture, size=(self.square_size, self.square_size))

    def on_size(self, instance=None, value=None):
        self.square_size = int(min(self.size) / 8)
        self.board_size = self.square_size * 8
        self.bottom_left = (int((self.width - self.board_size) / 2 + self.pos[0]), int((self.height - self.board_size) / 2 + self.pos[1]))
        # Generate textures
        self.piece_textures = {}
        for piece in 'klmnopqrstuvHIJKLMNOPQRS':
            self.piece_textures[piece] = Label(text=piece, font_name='img/ChessCases.ttf', font_size=self.square_size)
            self.piece_textures[piece].texture_update()
        self._draw_board()
        self._draw_pieces()

    def on_pos(self, instance, value):
        self.bottom_left = (int((self.width - self.board_size) / 2 + self.pos[0]), int((self.height - self.board_size) / 2 + self.pos[1]))
        self._draw_board()
        self._draw_pieces()

    def _animate_piece(self, touch, pos):
        # this is handled elsewhere, right?
        return
        """
        self._draw_board()
        self._draw_pieces(skip=self._moving_piece_from)
        self._draw_piece(self._moving_piece, pos)
        """

    def mouse_callback(self, instance, value):
        touch = Touch(value[0],value[1])
        square = self._to_square(touch)
        # print "square: {0}".format(square)
        if 0 <= square <= 63:
            if not self.app.use_engine:
                hint_move = self.app.hint_move
        else:
            if not self.app.use_engine:
                self._draw_board()
                self._draw_pieces()
                self.app.hint_move = None
            # for sq in to_square_list:
            #     self._highlight_square(sq)

    def __init__(self, app, **kwargs):
        super(ChessBoardWidget, self).__init__(**kwargs)
        self.app = app
        self.board = Board()
        """
        self.aa = None
        self.bb = 'rnbqr-k- pp---pbp --pp-np- ----p--- ---PP-P- --N-BP-- PPPQN--P --KR-B-R B 6 0 0 0 0 0 281 BigLion micker 0 1 0 39 39 51 52 9 P/g2-g4 (0:02) g4 0 1 0'
        self.cc = self.bb.split()
        self.board.reset_style12(self.bb)
        for aaa in self.board.position:
            for aaaa in aaa:
                print aaaa
        sys.exit(1)
        """
        self.app.board = self.board
        self.board.app = self.app # textbook OO
        self.last_move_san = None
        self.light = (1, 0.808, 0.620)
        # self.light =  (Image(LIGHT_SQUARE+"fir-lite.jpg"))
        self.dark =(0.821, 0.545, 0.278)
        self.light_img =  Image(source=LIGHT_SQUARE+"fir-lite.jpg")
        self.dark_img = Image(source=DARK_SQUARE+"wood-chestnut-oak2.jpg")

        self.black = (0, 0, 0)
        self.white = (1, 1, 1)
        self.highlight_color = (0.2, 0.710, 0.898)
        self.fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.always_promote_to_queen = True
        self.set_position(self.fen)
        self._background_textures = { 'K':'k', 'Q':'l', 'R':'m', 'B':'n', 'N':'o', 'P':'p', 'k':'q', 'q':'r', 'r':'s', 'b':'t', 'n':'u', 'p':'v'}
        self._front_textures = { 'K':'H', 'Q':'I', 'R':'J', 'B':'K', 'N':'L', 'P':'M', 'k':'N', 'q':'O', 'r':'P', 'b':'Q', 'n':'R', 'p':'S'}
        self.bind(_moving_piece_pos=self._animate_piece)
        self.on_size()
        Window.bind(mouse_pos=self.mouse_callback)


    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, g):
        if self._game is not None:
            self._game.unbind(moves=self._update_position)
            self._game.unbind(start_position=self._update_position)
        self._game=g
        g.bind(moves=self._update_position)
        g.bind(start_position=self._update_position)

    #TODO http://kivy.org/docs/guide/inputs.html

    def on_touch_down(self, touch):
        print "in on touch down: %s" % str(datetime.datetime.now())
        # push the current coordinate, to be able to restore it later
        # touch.push()

        # transform the touch coordinate to local space
        #touch.apply_transform_2d(self.to_local)

        """
        What is this?
        """
        ret = True
        """
        # dispatch the touch as usual to children
        # the coordinate in the touch is now in local space
        ret = super(ChessBoardWidget, self).on_touch_down(touch)
        if not self.collide_point(*touch.pos):
            touch.pop()
            return ret
        """
        square = self._to_square(touch)
        if self.position[square] == '.' or (self._moving_piece.isupper() if self.position[square].islower() else self._moving_piece.islower()):
            return

        tomove = self.fen.split()[1]

        if square == -1:
            self._moving_piece = '.'
            return
        else:
            if tomove == "w":
                if self.position[square].isupper():
                    self._moving_piece = self.position[square]
            else:
                if self.position[square].islower():
                    self._moving_piece = self.position[square]

        if self._moving_piece == '.':
            return
        # print "moving_piece:"
        # print self._moving_piece
        self._moving_piece_from = square
        """
        self._draw_board()
        self._draw_pieces()
        self._highlight_square(square)
        """

        #touch.pop()
        return ret

    def on_touch_move(self, touch):
        # TODO P3 make dragging an option for mobile
        # Right now disabling because it's too slow
        if not self.app.is_desktop():
            return

        coords = self._to_coordinates(self._to_square(touch))

        if self._moving_piece == '.':
            return
        self._draw_board()
        self._draw_pieces(skip=self._moving_piece_from)
        # self._highlight_square(self._moving_piece_to)

        if (self.app.is_desktop()):
            self._draw_piece(self._moving_piece, (touch.x - self.square_size / 2, touch.y - self.square_size / 2))
        else:
            self._draw_piece(self._moving_piece, (coords[0], coords[1]))

        self._highlight_square(self._moving_piece_from)
        # print touch

        return super(ChessBoardWidget, self).on_touch_move(touch)

    @staticmethod
    def square_name(i):
        return 'abcdefgh'[i % 8] + str(8 - i / 8)

    @staticmethod
    def square_number(name):
        return 'abcdefgh'.index(name[0]) + (8-int(name[1]))*8

    def on_touch_up(self, touch):
        print "in on touch up: %s" % str(datetime.datetime.now())
        square = self._to_square(touch)
        if square == -1 or not self.collide_point(*touch.pos):
            return

        move = self.square_name(self._moving_piece_from) + self.square_name(square)
        
        self.make_move(move)

        touch.ungrab(self)

        return True

    def make_move(self, move, is_auto=False):
        print "move is %s " % move

        from_square = self.square_number(move[:2])
        square = self.square_number(move[2:])
        coords = self._to_coordinates(square)

        if is_auto is True:
            self._moving_piece = self.position[from_square]
            self.position = self.position[:from_square]+"."+self.position[from_square+1:]

        # print "move : {0}".format(move)
        if self._moving_piece == '.':
            if move[:2] == 'h9':
                # Not legal square
                # print "not legal square"
                if not self.app.use_engine and self.app.hint_move:
                    if self.square_name(square) in self.app.hint_move:
                        move = self.app.hint_move
                else:
                    if self.app.engine_highlight_move and self.square_name(square) in self.app.engine_highlight_move:
                        move = self.app.engine_highlight_move
                if move[:2] == 'h9':
                    return
            else:
                move = move[-2:] + move[:2]
        # print "move_after_some-processing: {0}".format(move)
        if self.square_name(self._moving_piece_from) == self.square_name(square):
            self.on_size() # kind of a hack to trigger a refresh so the piece snaps to square
            if not self.app.use_engine:
                if self.app.hint_move and self.square_name(square) in self.app.hint_move:
                    move = self.app.hint_move
            else:
                if self.app.engine_highlight_move and self.square_name(square) in self.app.engine_highlight_move:
                    move = self.app.engine_highlight_move

        # print "move after hint : {0}".format(move)
        if move:
            if move[:2] != self.square_name(square) and move[-2:] != self.square_name(square):
                print "hint move not applicable"
                return
            if move[:2] == move[-2:]:
                return
        else:
            return

        # print "legal check"
        self._moving_piece_pos[0], self._moving_piece_pos[1] = self._to_coordinates(
            self._moving_piece_from) if self._animate_from_origin else coords


        print "animating: %s" % str(datetime.datetime.now())
        animation = Animation(_moving_piece_pos=self._to_coordinates(square), duration=0.1, t='in_out_sine')
        animation.move = move
        animation.bind(on_complete=self._update_after_animation)
        animation.start(self)
        self.app.hint_move = None
        # print('MOVE : ' + move)

        return True

class Touch(object):
    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y


class CustomListItemButton(ListItemButton):
    def __init__(self, **kwargs):
        # self.bind(height = self._resize)
        super(CustomListItemButton, self).__init__(**kwargs)
        # self.height = 10
        # with self.canvas.before:
        #     # grid.canvas.clear()
        #     Color(1, 1, 1)
        #     self.background = Rectangle()
            # Rectangle(size=Window.size)
        self.markup = True
        # self.selected_color = (0,0,0,0)
        self.border = (0,0,0,0)
        self.deselected_color = (1,1,1, 1)
        self.background_color = (1,1,1, 1)
        self.background_normal = 'img/background_normal.png'
        # self.background_down = 'img/background_pressed.png'
        # self.background_down = 'img/background_pressed.png'

    # def _resize(self,instance, height):
    #     # start with simple case of calculating scalefactor from height
    #     # print height
    #     # print self.size[1]
    #     # scalefactor = self.size[1]*1.0/height
    #     # print scalefactor
    #     self.font_size = '{0}dp'.format(self.height *0.4)
    #     # self.font_size = height * 0.35

class PositionEval(object):
    def __init__(self, informant_eval, integer_eval):
        self.informant_eval = informant_eval
        self.integer_eval = integer_eval
    def __str__( self):
        return "{0}, {1}".format(self.informant_eval, self.integer_eval)

pos_evals = [PositionEval("-+", -2), PositionEval("=+", -1), PositionEval("=", 0), PositionEval("+=", 1), PositionEval("+-", 2), PositionEval("none", 5)]

class SettingsScreen(Screen):
    pass

class ChessPiece(Scatter):
    image = ObjectProperty()
    moving = BooleanProperty(True)
    allowed_to_move = BooleanProperty(False)

    hide = BooleanProperty(False)

    def __init__(self, image_source, **kwargs):
        super(ChessPiece, self).__init__(**kwargs)

        self.image = Image(source=image_source)
        self.image.allow_stretch = True
        self.image.keep_ratio = True

        self.add_widget(self.image)
        self.auto_bring_to_front = True

    def on_hide(self, *args):
        self.remove_widget(self.image)

        if not self.hide:
            self.add_widget(self.image)

    def set_size(self, size):
        # Set both sizes otherwise the image
        # won't sit properly, and the scatter becomes larger than
        # the image.
        self.size = size[0], size[1]
        self.image.size = size[0], size[1]
        # self.scale = 0.9

    def set_pos(self, pos):
        self.pos = pos[0], pos[1]

    def on_touch_move(self, touch):
        # TODO P3 make dragging an option for mobile
        # Right now disabling because it's too slow
        if not self.is_desktop():
            return
        if not self.allowed_to_move:
            return
        if super(ChessPiece, self).on_touch_move(touch):
            self.moving = True
        #     self.image.size = self.size[0]*1.2, self.size[1]*1.2

    def on_touch_up(self, touch):
        print "in on_touch_up att: %s" % str(datetime.datetime.now())
        if super(ChessPiece, self).on_touch_up(touch):
#            if self.parent and self.moving:
#                app.check_piece_in_square(self)

            self.moving = False

    def on_touch_down(self, touch):
        print "in on_touch_down att: %s" % str(datetime.datetime.now())
        if super(ChessPiece, self).on_touch_down(touch):
            pass

class ChessSquare(Button):
    coord = NumericProperty(0)
    piece = ObjectProperty(None, allownone=True)
    show_piece = BooleanProperty(True)
    show_coord = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ChessSquare, self).__init__(**kwargs)

    def add_piece(self, piece):
        self.remove_widget(self.piece)
        self.piece = piece
        # print self.size
        if self.piece:
            self.piece.hide = not self.show_piece
            self.add_widget(piece)
            # print self.size
            piece.set_size(self.size)
            piece.set_pos(self.pos)

    def remove_piece(self):
        if self.piece:
            self.remove_widget(self.piece)


    def on_size(self, instance, size):
        # print 'Size: %s' % ( size)
        if self.piece:
            self.piece.set_size(size)


    def on_pos(self, instance, pos):
        # print '%s Positions: %s' % (get_square_abbr(self.coord), pos)
        if self.piece:
            self.piece.set_pos(pos)

class DataItem(object):
    def __init__(self, text='', is_selected=False):
        self.text = text
        self.is_selected = is_selected

class Knave(App):
    def generate_settings(self):
        def go_to_setup_board(value):
            self.root.current = 'setup_board'

        settings_panel = Settings() #create instance of Settings

        engine_panel = SettingsPanel(title="Engine") #create instance of left side panel
        board_panel = SettingsPanel(title="Board") #create instance of left side panel
        setup_pos_item = SettingItem(panel=board_panel, title="Input FEN") #create instance of one item in left side panel
        setup_board_item = SettingItem(panel=board_panel, title="Setup Board") #create instance of one item in left side panel
        setup_board_item.bind(on_release=go_to_setup_board)

        """
        database_panel = SettingsPanel(title="Database") #create instance of left side panel
        self.db_open_item = SettingItem(panel=board_panel, title="Open Database") #create instance of one item in left side panel
        self.db_open_item.bind(on_release=self.open_database)

        self.ref_db_open_item = SettingItem(panel=board_panel, title="Open Reference Database") #create instance of one item in left side panel
        self.ref_db_open_item.bind(on_release=self.open_database)

        database_panel.add_widget(self.db_open_item)
        database_panel.add_widget(self.ref_db_open_item)

        fen_input = TextInput(text="", focus=False, multiline=False, use_bubble = True)

        def on_level_value(slider, value):
            # self.level_label.text=value
            # print slider.value
            # print type(value)
            self.level_label.text = "%d" % value

        def on_fen_input(instance):
            if self.chessboard.setFEN(instance.text):
                self.start_pos_changed = True
                self.custom_fen = instance.text

        fen_input.bind(on_text_validate=on_fen_input)

        setup_pos_item.add_widget(fen_input)
        level_item = SettingItem(panel=engine_panel, title="Level") #create instance of one item in left side panel
        level_slider = Slider(min=0, max=20, value=20, step=1)
        level_slider.bind(value=on_level_value)
        self.level_label = Label(text=self.engine_level)
        level_item.add_widget(level_slider)
        level_current = SettingItem(panel=engine_panel, title="Selected Level") #create instance of one item in left side panel
        level_current.add_widget(self.level_label)

        board_panel.add_widget(setup_pos_item) # add item1 to left side panel
        board_panel.add_widget(setup_board_item)

        engine_panel.add_widget(level_item) # add item2 to left side panel
        engine_panel.add_widget(level_current) # add item2 to left side panel

        settings_panel.add_widget(board_panel)
        settings_panel.add_widget(database_panel)

        settings_panel.add_widget(engine_panel) #add left side panel itself to the settings menu

        def go_back():
            self.root.current = 'main'
            if self.engine_level != self.level_label.text:
                self.engine_level = self.level_label.text
                sf.set_option('skill level', self.engine_level)

        settings_panel.on_close=go_back
        """

        return settings_panel # show the settings interface

    #TODO P1 remove type="main"
    def create_chess_board(self, squares, type="main"):
        """
        if type == "main":
            board_widget = GridLayout(cols=8, rows=8, spacing=1, padding=(10,10))
        else:
            board_widget = GridLayout(cols=8, rows=12, spacing=1, size_hint=(1, 1))
        """
        board_widget = GridLayout(cols=8, rows=12, spacing=1, size_hint=(1, 1))

        for i, name in enumerate(SQUARES):
            bt = ChessSquare(keep_ratio=True, size_hint_x=1, size_hint_y=1)
            bt.sq = i
            bt.name = name
            if i in light_squares:
                bt.sq_color = "l"
                bt.background_normal = LIGHT_SQUARE+"fir-lite.jpg"
                # marble
                # bt.background_normal = LIGHT_SQUARE+"marble_166.jpg"
            else:
#                bt.background_color = DARK_SQUARE
                bt.background_normal = DARK_SQUARE+"wood-chestnut-oak2.jpg"
                # marble
                # bt.background_normal = DARK_SQUARE+"marble_252.jpg"
                bt.sq_color = "d"
            bt.background_down = bt.background_normal

            """
            if type == "main":
                bt.bind(on_touch_down=self.touch_down_move)
                bt.bind(on_touch_up=self.touch_up_move)
            else:
                bt.bind(on_touch_down=self.touch_down_setup)
                bt.bind(on_touch_up=self.touch_up_setup)
            """
            squares.append(bt)
            board_widget.add_widget(bt)


        if type!="main":
            for index, i in enumerate([".", ".", ".", ".", ".", ".", ".", ".", ".", "R", "N", "B", "Q", "K", "P",  ".", ".", "r", "n", "b", "q", "k", "p", "."]):
                bt = ChessSquare()
                bt.sq = i
                bt.name = i
                # bt.sq_color = "l"

                if i!=".":
                    piece = ChessPiece(MERIDA+'%s.png' % IMAGE_PIECE_MAP[i])
                    bt.add_piece(piece)

                """
                bt.bind(on_touch_down=self.touch_down_setup)
                bt.bind(on_touch_up=self.touch_up_setup)
                """
                board_widget.add_widget(bt)

        return board_widget

    def update_clocks(self, *args):
        if self.engine_mode == ENGINE_PLAY:
            if self.lcd and self.computer_move_FEN_reached:
                self.write_to_lcd(self.format_time_strs(self.time_white, self.time_black),
                    clear = True)
            if self.engine_computer_move:
                self.update_time(color=self.engine_comp_color)
                self.engine_score.children[0].text = THINKING_TIME.format(self.format_time_str(self.time_white), self.format_time_str(self.time_black))

            else:
                self.update_player_time()
                if self.show_hint:
                    if not self.ponder_move_san and self.ponder_move and self.ponder_move!='(none)':
                        # print self.ponder_move
                        try:
                            self.ponder_move_san = self.get_san([self.ponder_move],figurine=True)[0]
                            # print "ponder_move_san: "+self.ponder_move_san
                            # if not self.spoke_hint:
                            #     self.spoke_hint = True
                            #     self.speak_move(self.ponder_move)
                        except IndexError:
                            self.ponder_move_san = "None"
                    if self.ponder_move_san:
                        self.engine_score.children[0].text = YOURTURN_MENU.format(self.ponder_move_san, self.eng_eval, self.format_time_str(self.time_white), self.format_time_str(self.time_black))
                        if not self.spoke_hint:
                            self.spoke_hint = True
                            self.speak_move(self.ponder_move, immediate=True)
                    else:
                        self.engine_score.children[0].text = YOURTURN_MENU.format("Not available", self.eng_eval, self.format_time_str(self.time_white), self.format_time_str(self.time_black))
                else:
                    self.engine_score.children[0].text = YOURTURN_MENU.format("hidden", "hidden", self.format_time_str(self.time_white), self.format_time_str(self.time_black))

    def update_grid_border(self, instance, width, height):
        with self.board_widget.canvas.before:
            # grid.canvas.clear()
            Color(0.5, 0.5, 0.5)
            Rectangle(size=Window.size)

    def update_database_display(self, game, ref_game=None):
        game = self.get_grid_click_input(game, ref_game)
        if game == SHOW_GAMES or game == SHOW_REF_GAMES:
            if self.database_display:
                self.database_panel.reset_grid()
            self.database_display = True
            if not self.database_display:
                self.db_stat_label.text = "No Games"
                self.db_adapter.data = {}
            if game == SHOW_REF_GAMES:
                self.use_ref_db = True
                self.update_database_panel()
            else:
                self.use_ref_db = False
                self.update_database_panel()
            # self.update_book_panel()
            # self.database_display = False

    def get_token(self, tokens, index):
        try:
            return tokens[index]
        except IndexError:
            return '*'

    def on_load(self, i):
        # REMOVE
        print "in on load"
        self.connection = FICSConnection("freechess.org",[5000],"guest","",None,self)
        self.board_manager = BoardManager(self.connection)
        print "starting connection"
        self.connection.start()
        print "connection started"
        #sys.exit(1)

        import threading
        threading.Timer(5,self.connection.client.run_command, ["ob /l"]).start()
        #self.connection.client.run_command("ob /l")

        # END REMOVE

        if not self.is_desktop:
            return
        if (len(sys.argv) < 1):
            if sys.argv[1] == "test":
#         if True:
#             if True:
                # hack because there doesn't appear to be a real on_load in kivy
                if (i != 2):
                    import threading
                    threading.Timer(2, self.on_load, [2]).start()
                else:
                    from test import Test
                    Test(self).run_all()

    def build(self):
        if (not self.is_desktop()):
            Config.set('postproc', 'retain_time', '10')
            Config.set('postproc', 'double_tap_time', '1')
            Config.set('postproc', 'triple_tap_time', '2')
            Config.set('graphics', 'fullscreen', 'auto')
            Config.write()

        self.connection = None
        self.board_manager = None
        self.custom_fen = None
        self.pyfish_fen = 'startpos'
        self.variation_dropdown = None
        self.start_pos_changed = False
        self.engine_mode = None
        self.engine_computer_move = True
        self.computer_move_FEN_reached = False

        self.engine_comp_color = 'b'
        self.engine_level = '20'
        self.time_last = None
        self.time_white = 0
        self.time_inc_white = 0
        self.time_black = 0
        self.time_inc_black = 0

        self.from_move = None
        self.to_move = None
        self.db_sort_criteria = []
        self.show_hint = False
        self.speak_move_queue = []

        self.ponder_move = None
        self.hint_move = None
        self.engine_highlight_move = None
        self.lcd_lock = RLock()
        self.lcd = None
        self.arduino = None

        self.ponder_move_san = None
        self.eng_eval = None

        self.train_eng_score = {}

        self.squares = []
        self.setup_board_squares = []
        self.use_engine = False
        self.use_ref_db = False
        self.stop_called = False
        # self.engine_running = False
        self.spoke_hint = False

        # Make this an option later
        self.use_tb = False

        self.book_display = True
        self.database_display = False
        self.user_book_display = True
        self.last_touch_down_move = None
        self.last_touch_up_move = None
        self.last_touch_down_setup = None
        self.last_touch_up_setup = None
        self.book = None
        # self.book = PolyglotOpeningBook("book.bin")

        Clock.schedule_interval(self.update_clocks, 1)

        #grandparent = GridLayout(size_hint=(1,1), cols=1, orientation = 'vertical')
        #parent = BoxLayout(spacing=1, orientation='vertical')
        parent = GridLayout(size_hint=(1,1), cols=1, orientation = 'vertical')
        # box = BoxLayout(spacing=10, padding=(10,10))
        self.board_widget = ChessBoardWidget(self)

            # self.create_chess_board(self.squares)

        # Dummy params for listener
        self.update_grid_border(0,0,0)
        Window.bind(on_resize=self.update_grid_border)

        #self.b = BoxLayout(size_hint=(0.15,0.15))
        self.controls_widget = BoxLayout(size_hint=(.5,.05))

        back_bt = Button(markeup=True)
        back_bt.text = "<"

        back_bt.bind(on_press=self.back)
        self.controls_widget.add_widget(back_bt)

        self.prev_move = Label(markup=True,font_name='img/CAChess.ttf',font_size=16)
        self.controls_widget.add_widget(self.prev_move)

        fwd_bt = Button(markeup=True)
        fwd_bt.text = ">"

        fwd_bt.bind(on_press=self.fwd)
        self.controls_widget.add_widget(fwd_bt)

        comment_bt = Button(markup=True)
        comment_bt.text = "!?"

        #comment_bt.bind(on_press=self.comment)
        self.controls_widget.add_widget(comment_bt)

        new_bt = Button(markeup=True)
        new_bt.text = "New"

        new_bt.bind(on_press=self.new)
        self.controls_widget.add_widget(new_bt)


        save_bt = Button(markup=True)
        save_bt.text = "Save"

        #save_bt.bind(on_press=self.save)
        self.controls_widget.add_widget(save_bt)

        """
        settings_bt = Button(markup=True, text='Setup')
        settings_bt.bind(on_press=self.go_to_settings)
        self.b.add_widget(settings_bt)
        """

        # box.add_widget()
        parent.add_widget(self.board_widget)
        parent.add_widget(self.controls_widget)

        platform = kivy.utils.platform()
        sm = ScreenManager(transition=SlideTransition())
        board_screen = Screen(name='main')
        #board_screen.add_widget(grandparent)
        board_screen.add_widget(parent)
        sm.add_widget(board_screen)

        settings_screen = SettingsScreen(name='settings')
        settings_screen.add_widget(self.generate_settings())

        sm.add_widget(settings_screen)

        setup_board_screen = Screen(name='setup_board')
        setup_widget = self.create_chess_board(self.setup_board_squares, type="setup")

        def go_to_main_screen(value):
            if self.root:
                self.root.current = 'main'

        def setup_board_change_tomove(value):
            if value.state == "normal":
                # print "black to move"
                self.setup_chessboard.turn = 'b'
            else:
                # print "white to move"
                self.setup_chessboard.turn = 'w'

        self.on_load(1)

        return sm

    def go_to_settings(self, instance):
        self.root.current='settings'

    def get_ref_tags(self, t):
        m = MarkupLabel(text=t.text)
        ref_tags = []
        for s in m.markup:
            if s.startswith(REF_) and s.endswith(']'):
                ref_tags.append(s.split(REF_)[1].strip(']'))

        return ref_tags

    def get_grid_click_input(self, mv, ref_move):
        if ref_move:
            mv = ref_move
        else:
            tags = self.get_ref_tags(mv)
            if tags:
                mv = tags[0]
            else:
                mv = mv.text
        return mv

    def reset_clock_update(self):
        self.time_last = datetime.datetime.now()

    def time_add_increment(self, color='w'):
        if color == 'w':
            self.time_white+=self.time_inc_white
        else:
            self.time_black+=self.time_inc_black

    def update_time(self, color='w'):
        current = datetime.datetime.now()
        seconds_elapsed = (current - self.time_last).total_seconds()
#        print "seconds_elapsed:{0}".format(seconds_elapsed)
        self.time_last = current
        if color == 'w':
            self.time_white-=seconds_elapsed
        else:
            self.time_black-=seconds_elapsed

    def reset_clocks(self):
#        self.white_time_now = time.clock()
#        self.black_time_now = time.clock()
        self.time_last = datetime.datetime.now()

        self.time_white = 60
        self.time_inc_white = 3
        self.time_black = 420
        self.time_inc_black = 8
        if self.engine_comp_color == 'b':
            # Swap time allotments if comp is black (comp gets less time)
            self.time_white, self.time_black = self.time_black, self.time_white
            self.time_inc_white, self.time_inc_black = self.time_inc_black, self.time_inc_white

    def is_desktop(self):
        platform = kivy.utils.platform()
#        print platform
        return True if platform.startswith('win') or platform.startswith('linux') or platform.startswith('mac') else False

    def is_mac(self):
        platform = kivy.utils.platform()
        return True if platform.startswith('mac') else False

    def new(self, obj):
        return True


    def back(self, obj):
        return True

    def get_san(self, moves, figurine=False):
        prev_fen = sf.get_fen(self.pyfish_fen,  self.chessboard.get_prev_moves())

        move_list = sf.to_san(prev_fen, moves)
        if figurine:
            for i, m in enumerate(move_list):
                # print m
                m = self.convert_san_to_figurine(m)
                # print m
                move_list[i] = m
        return move_list

    # def format_time_str(self,time_a, separator='.'):
    #     return "%d%s%02d" % (int(time_a/60), separator, int(time_a%60))
    #
    def format_time_str(self, time_a):

        seconds = time_a
        # print "seconds: {0}".format(seconds)
        m, s = divmod(seconds, 60)
        # print "m : {0}".format(m)
        # print "s : {0}".format(s)

        if m >=60:
            h, m = divmod(m, 60)
            return "%d:%02d:%02d" % (h, m, s)
        else:
            # print "%02d:%02d" % (m, s)
            return "%02d:%02d" % (m, s)

    def format_time_strs(self, time_a, time_b, disp_length=16):
        fmt_time_a = self.format_time_str(time_a)
        fmt_time_b = self.format_time_str(time_b)

        head_len = len(fmt_time_a)
        tail_len = len(fmt_time_b)

        num_spaces = disp_length - head_len - tail_len

        return fmt_time_a+" "*num_spaces+fmt_time_b


    def speak_move(self, san, immediate=False):
        if self.is_mac():
            # print "best_move:{0}".format(best_move)
            # print sf.position()
            # try:
            #     san = self.get_san([best_move])[0]
            # except IndexError:
            #     return
            # print san
            spoken_san = san
            spoken_san = spoken_san.replace('O-O-O', ' castles long ')
            spoken_san = spoken_san.replace('+', ' check ')

            for k, v in SPOKEN_PIECE_SOUNDS.iteritems():
                spoken_san = spoken_san.replace(k, v)
            spoken_san = spoken_san.replace('x', ' captures ')
            spoken_san = spoken_san.replace('=', ' promotes to ')
            # print spoken_san
            if immediate:
                os.system("say " + spoken_san)
            else:
                if spoken_san not in self.speak_move_queue:
                    self.speak_move_queue.append(spoken_san)
            # os.system("say " + spoken_san)

    def update_engine_output(self, line):
        if not self.use_engine:
            # print "not using engine"
            # print line
            # parse best move
            self.hint_move, self.ponder_move = self.parse_bestmove(line)
            # self.grid._update_position(None, self.chessboard.position.fen)
            if self.hint_move:
                # print "hint_move : {0}".format(self.hint_move)
                self.board_widget._draw_board()
                self.board_widget._draw_pieces()
                self.board_widget._highlight_square_name(self.hint_move[-2:])
                self.board_widget._highlight_square_name(self.hint_move[:2])

        # print line

        if self.use_engine:
            output = self.engine_score
            if self.engine_mode == ENGINE_ANALYSIS:
                out_score = self.parse_score(line, figurine=True)
                #out_score = None
                if out_score:
                    first_mv, can_line, raw_line, cleaned_line = out_score
                    if first_mv:
                        self.board_widget._draw_board()
                        self.board_widget._draw_pieces()
                        self.board_widget._highlight_square_name(first_mv[-2:])
                        self.board_widget._highlight_square_name(first_mv[:2])
                        self.engine_highlight_move = first_mv
                        if cleaned_line:
                            # print "Cleaned line"
                            # print cleaned_line
                            output.children[0].text = cleaned_line
                        if raw_line:
                            output.raw = raw_line
                        if can_line:
                            output.can_line = can_line

            elif self.engine_mode == ENGINE_PLAY:
                if self.engine_computer_move:
                    best_move, self.ponder_move = self.parse_bestmove(line)
    #                            print "ponder_move:{0}".format(self.ponder_move)

                    depth, score = self.get_score(line)
                    if score:
                        self.eng_eval = score
                    # self.update_time(color=self.engine_comp_color)
                    if best_move:
                        self.process_move(best_move)
                        self.time_add_increment(color=self.engine_comp_color)

                        self.show_hint = False
                        self.spoke_hint = False
                        self.ponder_move_san = None
                        # se(best_move)
            elif self.engine_mode == ENGINE_TRAINING:

                output.children[0].text = THINKING
                best_move, self.ponder_move = self.parse_bestmove(line)
    #                            print "best_move:{0}".format(best_move)
    #                            print "ponder_move:{0}".format(self.ponder_move)

                depth, score = self.get_score(line)
                # print score

                if depth:
                    self.train_eng_score[depth] = score
                    # print "depth : {0}".format(depth)
                if best_move:
                    # print "best_move"
                    # print "training_score : {0}".format(score)
                    random_depth = random.randint(3, 10)
                    # print "random_depth : {0}".format(random_depth)
                    # print "san :{0}".format(best_move)
                    san = self.get_san([best_move], figurine=True)[0]
                    # print san
                    # print "san :{0}".format(san)
                    score = ""
                    if self.train_eng_score.has_key(random_depth):
                        score = self.train_eng_score[random_depth]
                    output.children[0].text = TRAIN_MENU.format(san, score)
                    self.train_eng_score = {}


    def write_to_lcd(self, message, clear = False):
        with self.lcd_lock:
            if len(message) > 32:
                message = message[:32]
            if len(message) > 16 and "\n" not in message:
                # Append "\n"
                message = message[:16]+"\n"+message[16:]
            # lcd.printString("                ", 0, 0)
            # lcd.printString("                ", 1, 0)
            if clear:
                self.lcd.printString("                ", 0, 0)
                self.lcd.printString("                ", 0, 1)

                # lcd.printString("      ",0,1)
            if "\n" in message:
                first, second = message.split("\n")
                # print first
                # print second
                self.lcd.printString(first, 0, 0)
                self.lcd.printString(second, 0, 1)
            else:
                self.lcd.printString(message, 0, 0)
            sleep(0.1)

    def select_variation(self, i):
        return True

    def fwd(self, obj):
        return True

    def touch_down_move(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return

        # print "touch_move"
        # print touch
        mv = img.name
        squares = self.chessboard.position

        if squares[mv]:
            self.last_touch_down_move = mv

    def touch_down_setup(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return

        # print "touch_move"
        # print touch
        mv = img.name
        self.last_touch_down_setup = mv

    def touch_up_setup(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return
        self.last_touch_up_setup = img.name
        if self.last_touch_up_setup and self.last_touch_down_setup and self.last_touch_up_setup != self.last_touch_down_setup:
#            print "touch_down_setup:"
#            print self.last_touch_down_setup
#            # print len(self.last_touch_down_setup)
#            print "touch_up_setup:"
#            print self.last_touch_up_setup
            # print len(self.last_touch_up_setup)
            if len(self.last_touch_down_setup)==1 and len(self.last_touch_up_setup)==2:
                sq = Square(self.last_touch_up_setup)
                self.setup_chessboard[sq] = Piece(self.last_touch_down_setup)
                self.fill_chess_board(self.setup_board_squares[SQUARES.index(self.last_touch_up_setup)], self.setup_chessboard[self.last_touch_up_setup])

            elif len(self.last_touch_down_setup)==2 and len(self.last_touch_up_setup)==1:
                del self.setup_chessboard[self.last_touch_down_setup]
                self.fill_chess_board(self.setup_board_squares[SQUARES.index(self.last_touch_down_setup)], self.setup_chessboard[self.last_touch_down_setup])

            elif len(self.last_touch_down_setup)==2 and len(self.last_touch_up_setup)==2:
                sq = Square(self.last_touch_up_setup)
                self.setup_chessboard[sq] = self.setup_chessboard[Square(self.last_touch_down_setup)]
                self.fill_chess_board(self.setup_board_squares[SQUARES.index(self.last_touch_up_setup)], self.setup_chessboard[self.last_touch_up_setup])
                del self.setup_chessboard[self.last_touch_down_setup]
                self.fill_chess_board(self.setup_board_squares[SQUARES.index(self.last_touch_down_setup)], self.setup_chessboard[self.last_touch_down_setup])

    def touch_up_move(self, img, touch):
        if not img.collide_point(touch.x, touch.y):
            return

        self.last_touch_up_move = img.name
        if self.last_touch_up_move and self.last_touch_down_move and self.last_touch_up_move != self.last_touch_down_move:
            self.process_move()

    def add_try_variation(self, move):
        #TODO: add move list
        return True

    def update_player_time(self):
        color = 'w'
        if self.engine_comp_color == 'w':
            color = 'b'
        self.update_time(color=color)

    def update_player_inc(self):
        color = 'w'
        if self.engine_comp_color == 'w':
            color = 'b'
        self.time_add_increment(color=color)

    def is_promotion(self, move):
        from_rank = move[1]
        to_rank = move[3]
        move_obj = Move(move[0:2],move[2:4])

        if from_rank == '7' and to_rank == '8' and str(self.board_widget.board.get_square(move_obj.source)) == 'P':
            return True

        if from_rank == '2' and to_rank == '1' and str(self.board_widget.board.get_square(move_obj.source)) == 'p':
            return True

        return False

    def add_promotion_info(self, move):
        # Promotion info already present?
        if len(move) > 4:
            return move
        else:
            # Auto queen for now
            return move + "q"

    def process_move(self, move=None):
        # print "process_move"
        # print "move:{0}".format(move)

        try:
            if not move:
                move = self.last_touch_down_move+self.last_touch_up_move
            if self.is_promotion(move):
                move = self.add_promotion_info(move)

            if self.engine_mode == ENGINE_PLAY:
                if not self.engine_computer_move:
                    # self.update_player_time()
                    self.update_player_inc()
                    # self.speak_move_queue.append(move)
                    self.engine_computer_move = True
                else:
                    self.engine_computer_move = False
            if self.engine_mode == ENGINE_PLAY:
                san = self.get_san([move])[0]
                self.speak_move(san)
        except Exception, e:
            print e
            raise
            # TODO: log error

    def generate_move_list(self, all_moves, eval = None, start_move_num = 1):
        score = ""
        if start_move_num % 2 == 0:
            turn_sep = '..'
        else:
            turn_sep = ''
        if eval is not None:
            score = str(eval) + " " + turn_sep

        for i, mv in it.izip(it.count(start_move_num), all_moves):
            if i % 2 == 1:
                score += "%d." % ((i + 1) / 2)
            if mv:
                score += "%s " % mv

        return score

    def database_action(self):
        print "action"
        pass

    def get_game_header(self, g, header, first_line=False):

        try:
            ref_db = self.use_ref_db
            if ref_db:
                record = self.ref_db_index_book.Get("game_{0}_data".format(g))
            else:
                record = self.db_index_book.Get("game_{0}_data".format(g))
            if header == "ALL":
                return record
            text = ""
            text = record.split("|")[DB_HEADER_MAP[header]]
            # try:
            #     j = json.loads(record, "latin-1")
            #     text = j[header]
            # except UnicodeDecodeError:
            #     print record
            # except ValueError:
            #     print record
            #     j = json.loads(repair_json(record), "latin-1")
            #     text = j[header]

            # text = self.db_index_book.Get("game_{0}_{1}".format(g,header))
            if first_line:
#                text = self.pgn_index["game_index_{0}".format(g)][header]
                if "," in text:
                    return text.split(",")[0]
            return text
#            return self.pgn_index["game_index_{0}".format(g)][header]
        except KeyError:
            return "Unknown"

    def fill_chess_board(self, sq, p):
#        print "p:%s"%p
#        print "sq:%s"%sq
#        if p == ".":
#            sq.remove_piece()
        if p:
            # print p.symbol
            piece = ChessPiece(MERIDA+'%s.png' % IMAGE_PIECE_MAP[p.symbol])
            sq.add_piece(piece)
        else:
            sq.remove_piece()

    def convert_san_to_figurine(self, san):
        for k, v in PIECE_FONT_MAP.iteritems():
            san = san.replace(k, v)
        return san

    def get_prev_move(self, figurine = True):
        return True

if __name__ == '__main__':
    Knave().run()
