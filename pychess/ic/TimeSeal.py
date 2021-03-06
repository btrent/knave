import errno
import socket
import telnetlib
import re
import random
import time
import platform
import getpass

from pychess.System.Log import Log

ENCODE = [ord(i) for i in "Timestamp (FICS) v1.0 - programmed by Henrik Gram."]
ENCODELEN = len(ENCODE)
G_RESPONSE = '\x029'
FILLER = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
IAC_WONT_ECHO = ''.join([telnetlib.IAC, telnetlib.WONT, telnetlib.ECHO])

class TimeSeal:
    BUFFER_SIZE = 4096
    sensitive = False

    def __init__(self):
        self.name = ""
        
    def open (self, host, port):
        if hasattr(self, "closed") and self.closed:
            return
        
        self.port = port
        self.host = host
        self.name = host

        self.FatICS = False

        self.connected = False
        self.closed = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stateinfo = None
        
        self.sock.settimeout(10)
        try:
            self.sock.connect((host, port))
        except socket.error, e:
            if e.errno != errno.EINPROGRESS:
                raise
        self.sock.settimeout(None)
        
        self.buf = ''
        self.writebuf = ''
        
        print >> self, self.get_init_string()
        self.cook_some()
    
    def close (self):
        self.closed = True
        if hasattr(self, "sock"):
            self.sock.close()
    
    def encode(self, inbuf, timestamp = None):
        assert inbuf == "" or inbuf[-1] != "\n"
        
        if not timestamp:
            timestamp = int(time.time()*1000 % 1e7)
        enc = inbuf + '\x18%d\x19' % timestamp
        padding = 12 - len(enc)%12
        filler = random.sample(FILLER, padding)
        enc += "".join(filler)
        
        buf = [ord(i) for i in enc]
        
        for i in range(0, len(buf), 12):
            buf[i + 11], buf[i] = buf[i], buf[i + 11]
            buf[i + 9], buf[i + 2] = buf[i + 2], buf[i + 9]
            buf[i + 7], buf[i + 4] = buf[i + 4], buf[i + 7]
        
        encode_offset = random.randrange(ENCODELEN)
        
        for i in xrange(len(buf)):
            buf[i] |= 0x80
            j = (i+encode_offset) % ENCODELEN
            buf[i] = chr((buf[i] ^ ENCODE[j]) - 32)
        
        buf.append( chr(0x80 | encode_offset))
        
        return ''.join(buf)

    def get_init_string(self):
        """ timeseal header: TIMESTAMP|bruce|Linux gruber 2.6.15-gentoo-r1 #9
            PREEMPT Thu Feb 9 20:09:47 GMT 2006 i686 Intel(R) Celeron(R) CPU
            2.00GHz GenuineIntel GNU/Linux| 93049 """  
        user = getpass.getuser()
        uname = ' '.join(list(platform.uname()))
        return  "TIMESTAMP|%(user)s|%(uname)s|" % locals()
    
    def decode(self, buf, stateinfo = None):
        expected_table = "[G]\n\r"
        # TODO: add support to FatICS's new zipseal protocol when it finalizes
        #expected_table = "[G]\n\r" if not self.FatICS else "[G]\r\n"
        final_state = len(expected_table)
        g_count = 0
        result = []
    
        if stateinfo:
            state, lookahead = stateinfo
        else:
            state, lookahead = 0, []
    
        lenb = len(buf)
        idx = 0
        while idx < lenb:
            ch = buf[idx]
            expected = expected_table[state]
            if ch == expected:
                state += 1
                if state == final_state:
                    g_count += 1
                    lookahead = []
                    state = 0
                else:
                    lookahead.append(ch)
                idx += 1
            elif state == 0:
                result.append(ch)
                idx += 1
            else:
                result.extend(lookahead)
                lookahead = []
                state = 0
    
        return ''.join(result), g_count, (state, lookahead)
    
    def write(self, str):
        self.writebuf += str
        if "\n" not in self.writebuf:
            return
        
        if self.closed:
            return
        
        i = self.writebuf.rfind("\n")
        str = self.writebuf[:i]
        self.writebuf = self.writebuf[i+1:]
        
        logstr = "*"*len(str) if self.sensitive else str
        Log.info(logstr+"\n", (self.name, "raw"))
        str = self.encode(str)
        self.sock.send(str+"\n")
    
    def readline(self):
        return self.readuntil("\n")
    
    def readuntil(self, until):
        while True:
            i = self.buf.find(until)
            if i >= 0:
                stuff = self.buf[:i+len(until)]
                self.buf = self.buf[i+len(until):]
                return stuff
            self.cook_some()
    
    def cook_some (self):
        recv = self.sock.recv(self.BUFFER_SIZE)
        if len(recv) == 0:
            return
        
        if not self.connected:
            Log.debug(recv, (self.name, "raw"))
            self.buf += recv
            
            if "FatICS" in self.buf:
                self.FatICS = True
            elif "Starting FICS session" in self.buf:
                self.connected = True
                self.buf = self.buf.replace(IAC_WONT_ECHO, '')
        
        else:
            recv, g_count, self.stateinfo = self.decode(recv, self.stateinfo)
            recv = recv.replace("\r","")
            Log.debug(recv, (self.name, "raw"))
            
            for i in range(g_count):
                print >> self, G_RESPONSE
            
            self.buf += recv
    
    def read_until (self, *untils):
        while True:
            for i, until in enumerate(untils):
                start = self.buf.find(until)
                if start >= 0:
                    self.buf = self.buf[:start]
                    return i
            self.cook_some()

            








