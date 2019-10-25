from os import *
from sys import *
from pickle import *
from io import open as Open 
from pickle import Unpickler as Unpkler
from pickle import Pickler as Pkler
black_type_list = [eval, execfile, compile, system, open, file, popen, popen2, popen3, popen4, fdopen,
                   tmpfile, fchmod, fchown, pipe, chdir, fchdir, chroot, chmod, chown, link,
                   lchown, listdir, lstat, mkfifo, mknod, mkdir, makedirs, readlink, remove, removedirs,
                   rename, renames, rmdir, tempnam, tmpnam, unlink, walk, execl, execle, execlp, execv,
                   execve, execvp, execvpe, exit, fork, forkpty, kill, nice, spawnl, spawnle, spawnlp, spawnlpe,
                   spawnv, spawnve, spawnvp, spawnvpe, load, loads]
class FilterException(Exception):
    def __init__(self, value):
        super(FilterException, self).__init__(
            'the callable object {value} is not allowed'.format(value=str(value)))
def _hook_call(func):
    def wrapper(*args, **kwargs):
        print args[0].stack
        if args[0].stack[-2] in black_type_list:
            raise FilterException(args[0].stack[-2])
        return func(*args, **kwargs)
    return wrapper
def LOAD(file):
    unpkler = Unpkler(file)
    unpkler.dispatch[REDUCE] = _hook_call(unpkler.dispatch[REDUCE])
    return Unpkler(file).load()
with Open("test","rb") as f:
	LOAD(f)
