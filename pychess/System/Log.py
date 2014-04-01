import os
import sys
import time

from pychess.Utils.const import LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR, STANDARD_LOGGING

class Log ():
        
    def _format (self, task, message, type):
        t = time.strftime ("%H:%M:%S")
        return "%s %s %s: %s" % (t, task, labels[type], message)
        
    def _log (self, task, message, type):
        if not message: return
            
        print message
        
    def debug (self, message, task="Default"):
        if DEBUG:
            self._log (task, message, LOG_DEBUG)
        
    def info (self, message, task="Default"):
        self._log (task, message, LOG_INFO)
        
    def warn (self, message, task="Default"):
        self._log (task, message, LOG_WARNING)
        
    def error (self, message, task="Default"):
        self._log (task, message, LOG_ERROR)


