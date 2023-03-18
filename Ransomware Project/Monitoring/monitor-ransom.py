#Detection and Prevention
#Get a list of all folders in C:\
#Create a perimeter file in all folders.   
#Watch these files for any modification
from hashlib import sha256
import os
import watchdog.events
import watchdog.observers
import time
import json
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
        sf, f = run_scandir(dir)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.abc'],
                                                             ignore_directories=False, case_sensitive=False)
  
    def on_modified(self, event):
        print("Watchdog Alert: Perimeter File Modified - % s." % event.src_path)
        
        x = input("Would you like to shutdown (y/n) ?")
        if x.lower() == 'y':
            #subprocess.run(["shutdown", "-s"])
            subprocess.run(["shutdown", "-f"])            
        # Event is modified, you can process it now
src_path = "C:\\test"
subfolders, files = run_scandir(src_path)
f = open(src_path+"\\checkfile.abc", "w") # in root directory
f.write("This is a perimeter file. Dont delete or modify")
f.close()
for each in subfolders:
    f = open(each+'\\'+"checkfile.abc", "w")
    f.write("This is a perimeter file. Dont delete or modify")
    f.close()
# Create checksums dictionary for all files
ckdict = {}
for each in files:
    try:
        ckdict[each] = hashfile(each)
    except:
        pass
try:
    with open('c:\\Users\\Public\\Documents\\checksums.txt','w') as fp:
        fp.write(json.dumps(ckdict))
except:
    print("Something went wrong")
            
event_handler = Handler()
observer = watchdog.observers.Observer()
observer.schedule(event_handler, path=src_path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

