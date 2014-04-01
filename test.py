from time import sleep
#from net.ics_connection import IcsConnection, FicsConnection
from pychess.ic.FICSConnection import FICSConnection
from pychess.ic.managers.BoardManager import BoardManager

class Test:
    app = None
    lines = None

    def __init__(self, app, **kwargs):
        self.app = app
        self.app.connection = FakeFICSConnection(app)
        self.load_data()
        self.bm = BoardManager(self.app.connection)

    def run_all(self):
        self.follow_game()

    def follow_game(self):
        print self.bm.parseStyle12("rkbrnqnb pppppppp -------- -------- -------- -------- PPPPPPPP RKBRNQNB W -1 1 1 1 1 0 161 GuestNPFS GuestMZZK -1 2 12 39 39 120 120 1 none (0:00) none 1 0 0", ("d","a"))
    
        """
        self.app.connection.parse_message('fortu, whom you are following, has started a game with theblob.')
        self.app.connection.parse_message('You are now observing game 408.')
        self.app.connection.parse_message('Game 408: theblob (1760) fortu (1795) rated lightning 1 0')

        for line in self.lines:
            print line
            #self.app.connection.parse_message(line)
            self.bm.parseStyle12(line)
            sleep(1)
        """

    def load_data(self):
        self.lines = [
            "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 60 60 1 none (0:00) none 0 0 0",
            "<12> rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 60 60 1 P/d2-d4 (0:00) d4 0 0 0",
            "<12> rnbqkbnr ppp-pppp -------- ---p---- ---P---- -------- PPP-PPPP RNBQKBNR W 3 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 60 60 2 P/d7-d5 (0:00) d5 0 1 0",
            "<12> rnbqkbnr ppp-pppp -------- ---p---- --PP---- -------- PP--PPPP RNBQKBNR B 2 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 59 60 2 P/c2-c4 (0:01) c4 0 1 212",
            "<12> rnbqkbnr ppp--ppp ----p--- ---p---- --PP---- -------- PP--PPPP RNBQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 59 60 3 P/e7-e6 (0:00) e6 0 1 157",
            "<12> rnbqkbnr ppp--ppp ----p--- ---p---- --PP---- --N----- PP--PPPP R-BQKBNR B -1 1 1 1 1 1 408 theblob fortu 0 1 0 39 39 59 60 3 N/b1-c3 (0:01) Nc3 0 1 212",
            "<12> rnbqkbnr ppp--ppp ----p--- -------- --pP---- --N----- PP--PPPP R-BQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 39 59 59 4 P/d5-c4 (0:00) dxc4 0 1 159",
            "<12> rnbqkbnr ppp--ppp ----p--- -------- --pP---- --N-P--- PP---PPP R-BQKBNR B -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 39 57 59 4 P/e2-e3 (0:01) e3 0 1 213",
            "<12> rnbqkbnr -pp--ppp p---p--- -------- --pP---- --N-P--- PP---PPP R-BQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 39 57 59 5 P/a7-a6 (0:00) a6 0 1 441",
            "<12> rnbqkbnr -pp--ppp p---p--- -------- --BP---- --N-P--- PP---PPP R-BQK-NR B -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 38 56 59 5 B/f1-c4 (0:01) Bxc4 0 1 213",
            ]

class FakeFICSConnection(FICSConnection):
    app = None

    def __init__(self, app, *args, **kwargs):
        self.app = app
        #super(self, *args, **kwargs)
        FICSConnection.__init__(self, "", "", "", "")

