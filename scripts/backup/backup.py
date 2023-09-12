#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
from datetime import datetime

date = datetime.now().strftime("%Y-%m-%d")

files = [
    'bermio',
    'bermio_nether',
    'bermio_the_end',
    'world',
    'world_nether',
    'world_the_end'
]

dir = sys.path[0] + "/../../../"

for i in range(len(files)):
    files[i] = dir + files[i]

dir     = sys.path[0] + "/../../backup/"+date
command = "mkdir -p "+dir

result  = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

for i in range(len(files)):
    command = "cp -R "+files[i]+" "+dir
    result  = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

dir     = dir + "/../"
folders = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]

print(folders)

