#Recovery program
import json
from hashlib import sha256
import os
import hashlib

def hashfile(file):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:   
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def run_scandir(dir):    # dir: str, ext: list
    subfolders = []
    files = []
    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            files.append(f.path)

    for dir in list(subfolders):
        f = run_scandir(dir)
        files.extend(f)
    return files

#recovery code

try:   
    with open('c:\\Users\\Public\\Documents\\checksums.txt','r') as json_file:
        ckdict = json.load(json_file)
except:
    print("No files available for recovery")
safe_files = open("C:\\Users\\Public\\Documents\\list_of_safe_files.txt", "w")
#verify checksums and create a list of unaffected files.
files = run_scandir("C:\\test")
for each in files:
    if each in ckdict:
        if hashfile(each) == ckdict[each]:
            safe_files.write(each+"\n") #save this file
            print(each+"\n") 
safe_files.close()
print("Recovery Complete. List of Safe files is C:\\Users\\Public\\Documents\\list_of_safe_files.txt")