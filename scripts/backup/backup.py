#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
from datetime import datetime

def _exec(command):
    subprocess.run(str(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

date = datetime.now().strftime("%Y-%m-%d")

# backup-ak egiteko munduak
files = [
    'bermio',
    'bermio_nether',
    'bermio_the_end',
    'world',
    'world_nether',
    'world_the_end'
]

# munduen path osoak hartu
dir = sys.path[0] + "/../../../"
for i in range(len(files)):
    files[i] = dir + files[i]

# backup-aren karpeta sortu
dir     = sys.path[0] + "/../../backup/"+date
command = 'mkdir -p "'+dir+'"'
_exec(command)

# backup-ak egin
for i in range(len(files)):
    command = 'cp -R "'+files[i]+'" "'+dir+'"'
    _exec(command)

# backup-en zerrenda lortu
dir     = dir + "/../"
folders = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
folders.sort(key=lambda x: os.path.getmtime(x), reverse=True)

# azken 15 backup-ak bakarrik utzi
remove_folders = folders[15:]
for i in range(len(remove_folders)):
    command = 'rm -rf "'+remove_folders[i]+'"'
    _exec(command)