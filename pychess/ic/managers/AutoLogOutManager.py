

class AutoLogOutManager ():

    
    def __init__ (self, connection):

        self.connection = connection
        
        self.connection.expect_line (self.onLogOut,
           "\*\*\*\* Auto-logout because you were idle more than \d+ minutes\. \*\*\*\*")
        self.connection.expect_line (self.onLogOut, "Logging you out\.")
        self.connection.expect_line (self.onLogOut,
           "\*\*\*\* .+? has arrived - you can't both be logged in\. \*\*\*\*")
    
    def onLogOut (self, match):
        print "Logout"
