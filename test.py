import re
from time import sleep
#from net.ics_connection import IcsConnection, FicsConnection
from pychess.ic.FICSConnection import FICSConnection
from pychess.ic.managers.BoardManager import BoardManager

class Test:
    app = None
    lines = None

    def __init__(self, app, **kwargs):
        self.app = app
        #self.app.connection = FakeFICSConnection(app)
        self.app.connection = FICSConnection("","","","",None,app)
        self.load_data()
        self.bm = BoardManager(self.app.connection)

    def run_all(self):
        self.follow_game()

    def follow_game(self):
        #print self.bm.parseStyle12("rkbrnqnb pppppppp -------- -------- -------- -------- PPPPPPPP RKBRNQNB W -1 1 1 1 1 0 161 GuestNPFS GuestMZZK -1 2 12 39 39 120 120 1 none (0:00) none 1 0 0", ("d","a"))
    
        """
        self.app.connection.parse_message('fortu, whom you are following, has started a game with theblob.')
        self.app.connection.parse_message('You are now observing game 408.')
        self.app.connection.parse_message('Game 408: theblob (1760) fortu (1795) rated lightning 1 0')
        """

        for line in self.lines:
            #print line
            match = re.search(r'<12> (.*)', line)
            self.bm.onStyle12(match)
            sleep(1)

    def load_data(self):
        self.lines = [
            "<12> rnbqkbnr pppppppp -------- -------- ----P--- -------- PPPP-PPP RNBQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 60 60 1 none (0:00) none 0 0 0",
            "<12> rnbqkbnr pppppppp -------- -------- ----P--- -------- PPPP-PPP RNBQKBNR B 3 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 60 60 1 P/e2-e4 (0:00) e4 0 0 0",
            "<12> rnbqkbnr pppp-ppp -------- ----p--- ----P--- -------- PPPP-PPP RNBQKBNR W 3 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 60 60 2 P/e7-e5 (0:00) e5 0 1 0",
        #    ]
        #self.aaa = [
            "<12> rnbqkbnr pppp-ppp -------- ----p--- ----P--- -----N-- PPPP-PPP RNBQKB-R B 2 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 59 60 2 N/g1-f3 (0:01) Nf3 0 1 212",
            "<12> rnbqkb-r pppp-ppp -----n-- ----p--- ----P--- -----N-- PPPP-PPP RNBQKB-R W -1 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 59 60 3 N/g8-f6 (0:00) Nf6 0 1 157",
            "<12> rnbqkb-r pppp-ppp -----n-- ----p--- --B-P--- -----N-- PPPP-PPP RNBQK--R B -1 1 1 1 1 1 408 theblob fortu 0 1 0 39 39 59 60 3 B/f1-c4 (0:01) Bc4 0 1 212",
            "<12> rnbqk--r pppp-ppp -----n-- --b-p--- --B-P--- -----N-- PPPP-PPP RNBQK--R W -1 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 59 59 4 B/f8-c5 (0:00) Bc5 0 1 159",
            "<12> rnbqk--r pppp-ppp -----n-- --b-p--- --B-P--- -----N-- PPPP-PPP RNBQ-RK- B -1 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 57 59 4 o-o (0:01) O-O 0 1 213",
            "<12> rnbqk--r pppp-ppp -----n-- ----p--- --B-P--- -----N-- PPPP-bPP RNBQ-RK- W -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 39 57 59 5 B/c5-f2 (0:00) Bxf2+ 0 1 441",
            "<12> rnbqk--r pppp-ppp -----n-- ----p--- --B-P--- -----N-- PPPP-RPP RNBQ--K- B -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 36 56 59 5 R/f1-f2 (0:01) Rxf2 0 1 213",
            "<12> rnbqk--r -ppp-ppp -----n-- p---p--- --B-P--- -----N-- PPPP-RPP RNBQ--K- W -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 36 56 59 6 P/a7-a5 (0:01) a5 0 1 213",
            "<12> rnbqk--r -ppp-ppp -----n-- p---p--- --B-P--- -----N-- PPPP--PP RNBQ-RK- B -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 36 56 59 6 R/f2-f1 (0:01) Rf1 0 1 213",
            "<12> rnbqk--r -ppp-ppp -----n-- ----p--- p-B-P--- -----N-- PPPP--PP RNBQ-RK- W -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 36 56 59 7 P/a5-a4 (0:01) a4 0 1 213",
            "<12> rnbqk--r -ppp-ppp -----n-- ----p--- pPB-P--- -----N-- P-PP--PP RNBQ-RK- B -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 36 56 59 7 P/b2-b4 (0:01) b4 0 1 213",
            "<12> rnbqk--r -ppp-ppp -----n-- ----p--- --B-P--- -p---N-- P-PP--PP RNBQ-RK- W -1 1 1 1 1 0 408 theblob fortu 0 1 0 37 36 56 59 8 P/a4-b3 (0:01) axb3 0 1 213",

            ]

        """
        self.lines = [
            "<12> rnbqkbnr pppppppp -------- -------- -------- -------- PPPPPPPP RNBQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 39 Nf6 60 60 1 none (0:00) none 0 0 0",
            "<12> rnbqkbnr pppppppp -------- -------- ---P---- -------- PPP-PPPP RNBQKBNR B 3 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 60 60 1 P/d2-d4 (0:00) d4 0 0 0",
            "<12> rnbqkbnr ppp-pppp -------- ---p---- ---P---- -------- PPP-PPPP RNBQKBNR W 3 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 60 60 2 P/d7-d5 (0:00) d5 0 1 0",
            "<12> rnbqkbnr ppp-pppp -------- ---p---- --PP---- -------- PP--PPPP RNBQKBNR B 2 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 59 60 2 P/c2-c4 (0:01) c4 0 1 212",
            "<12> rnbqkbnr ppp--ppp ----p--- ---p---- --PP---- -------- PP--PPPP RNBQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 39 39 59 60 3 Bc5 (0:00) e6 0 1 157",
            "<12> rnbqkbnr ppp--ppp ----p--- ---p---- --PP---- --N----- PP--PPPP R-BQKBNR B -1 1 1 1 1 1 408 theblob fortu 0 1 0 39 39 59 60 3 N/b1-c3 (0:01) Nc3 0 1 212",
            "<12> rnbqkbnr ppp--ppp ----p--- -------- --pP---- --N----- PP--PPPP R-BQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 39 59 59 4 P/d5-c4 (0:00) dxc4 0 1 159",
            "<12> rnbqkbnr ppp--ppp ----p--- -------- --pP---- --N-P--- PP---PPP R-BQKBNR B -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 39 57 59 4 O-O (0:01) e3 0 1 213",
            "<12> rnbqkbnr -pp--ppp p---p--- -------- --pP---- --N-P--- PP---PPP R-BQKBNR W -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 39 57 59 5 P/a7-a6 (0:00) a6 0 1 441",
            "<12> rnbqkbnr -pp--ppp p---p--- -------- --BP---- --N-P--- PP---PPP R-BQK-NR B -1 1 1 1 1 0 408 theblob fortu 0 1 0 38 38 56 59 5 B/f1-c4 (0:01) Bxc4 0 1 213",
            ]
        """

"""
class FakeFICSConnection(FICSConnection):
    app = None

    def __init__(self, app, *args, **kwargs):
        self.app = app
        #super(self, *args, **kwargs)
        FICSConnection.__init__(self, "", "", "", "")
"""
