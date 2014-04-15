import os
import sys
import time

import kivy.utils

from pychess.Utils.const import LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR, STANDARD_LOGGING

class Log ():
      
    DEBUG = True
    labels = {
        LOG_DEBUG: 'DEBUG',
        LOG_INFO: 'INFO',
        LOG_WARNING: 'WARNING',
        LOG_ERROR: 'ERROR',
    }
  
    @staticmethod
    def _format (task, message, type):
        t = time.strftime ("%H:%M:%S")
        return "%s %s %s: %s" % (t, task, Log.labels[type], message)
        
    @staticmethod
    def _log (task, message, type):
        try:
            print message
        except:
            pass
        if not message: 
            return

        if kivy.utils.platform().startswith('and'):
            return
            
        # temporarily disabling
        print Log._format(task, message, LOG_DEBUG)

    @staticmethod
    def debug (message, task="Default"):
        if Log.DEBUG:
            Log._log (task, message, LOG_DEBUG)
        
    @staticmethod
    def info (message, task="Default"):
        Log._log (task, message, LOG_INFO)
        
    @staticmethod
    def warn (message, task="Default"):
        Log._log (task, message, LOG_WARNING)
        
    @staticmethod
    def error (message, task="Default"):
        Log._log (task, message, LOG_ERROR)


