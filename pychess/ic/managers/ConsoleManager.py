

from pychess.ic.VerboseTelnet import ConsoleHandler


class ConsoleManager ():
    
    
    def __init__ (self, connection):
        self.connection = connection
        self.connection.client.consolehandler = ConsoleHandler(self.onConsoleMessage)

    def onConsoleMessage (self, line, block_code):
        pass
        #self.emit("consoleMessage", line, block_code)
