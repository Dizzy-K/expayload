#!/usr/bin/env python

#coding = UTF - 8
import base64
import json
import requests# 代理设置
proxy = 'http://127.0.0.1:8080'
use_proxy = False
MY_PROXY = None
if use_proxy:
    MY_PROXY = {
        'http': proxy,
        'https': proxy,
    }
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    'Upgrade-Insecure-Requests': '1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,ja;q=0.9,zh-HK;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
}
my_cookie = {}
def http_req(url, data = None, method = 'GET', params = None, json =
        False, cookies = None, proxies = MY_PROXY):
    if json:
        method = 'POST'
        json = data
        data = None
    if method == 'GET':
        params = data
        data = None
    r = requests.request(method, url, headers = headers, verify = False,
        json = json, params = params, data = data, cookies = cookies, proxies = MY_PROXY)
    return r

def graph_req(url, body):
    body = {
        'query': body
    }
    r = http_req(url, data = body, json = True)
    return r.json()

url = "http://localhost:8800/graphql"

def base64_decode(base_table):
    '''
    base64的6位索引转换为字符串
    '''
    bases = ''.join(base_table)
    bytes_len = int(len(bases) / 8)
    byte_table = [bases[i * 8: (i + 1) * 8]
        for i in range(bytes_len)
    ]
    # bases2 = ''.join(byte_table)
    # if bases != bases2: 
    #print('error...')
    char_table = [int(b, 2) for b in byte_table]
    return char_table

def decode_one(tbl, idx):
    tbl = ['{0:06b}'.format(i) for i in tbl]
    rtbl = base64_decode(tbl)
    s = ''.join([chr(i) for i in rtbl])
    r = graph_req(url, '''
            query {
            checkPass(memoId: 2,
                password: "%s")
        }
        ''' % s)
    message = r['errors'][0]['message']
    print(idx, message)
    valid_code = message.split("'")[1][3]
    return valid_code# 获取base64编码表

base_tbl = []

for c in range(64):
    tbl = [0 b111111, 0 b111111, 0 b011011, c]
    valid_code = decode_one(tbl, c)
    base_tbl.append(valid_code)

# padding字符
valid_code = decode_one([0 b111111, 0 b111111, 0 b011011], -1)
base_tbl.append(valid_code)
base_tbl = ''.join(base_tbl)

std_b64_table =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

def decode(s):
    table = str.maketrans(base_tbl, std_b64_table)
    new_s = s.translate(table)
    new_s += "="
    result = base64.b64decode(bytes(new_s, 'utf-8'))
    return str(result, 'utf-8')

print('password:', decode('要有了产于了主方以定人方于有成以他的爱爱'))
print('flag:', decode(
    '到年种成到定过成个他成会为而时方上而到年到年以可为多为而到可对方生而以年为有到成上可我行到他的面为们方爱'))
