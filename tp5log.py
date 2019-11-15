#! /usr/bin/env python
import requests, time

def get5log():
    end = 17
    url = "http://183.129.189.60:10041/runtime/log/201909/"
    file = url[-6:-1]
    for i in range(0, end):
        time.sleep(1)
        u = url+f"{i}.log"
        if (i < 10):
            u = url + f"0{i}.log"
        print(u)
        res = requests.get(u)
        res.close()
        if res.status_code == 200:
            print(f"sava log {i}.txt")
            filename = f"{file}_{i}.txt"
            with open(filename,'w+',encoding="utf-8") as f:
                f.write(res.text)
        else:
            print(f"{i}.log not exists")

if __name__ == "__main__":
    get5log()
