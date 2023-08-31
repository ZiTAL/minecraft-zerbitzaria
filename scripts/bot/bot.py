#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip3 install -U Mastodon.py
# pip3 install -U python-telegram-bot

import sys
import subprocess
import re
from   time     import time
from   mastodon import Mastodon
from   telegram import Bot

file = sys.path[0] + "/../../../logs/latest.log"
wait = 1

def readLog(filename):
    start_time   = int(time())
    tail_process = subprocess.Popen(["tail", "-F", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        start_reading = False

        while True:
            line = tail_process.stdout.readline().decode("utf-8")

            if(start_reading==False):
                execution_time = int(time())
                if(execution_time - start_time)>wait:
                    start_reading = True

            if(start_reading):
                if line and start_reading:
                    processMessage(line)

    except KeyboardInterrupt:
        tail_process.terminate()

def processMessage(line):
    # [16:11:29] [Server thread/INFO]: arkkuso joined the game
    # [16:11:29] [Server thread/INFO]: arkkuso left the game
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+(.*?)\s+(joined|left)", line, re.IGNORECASE)
    if(m):
        user = m.group(1)
        type = m.group(2)

        if(type=='joined'):
            msg = user+" zerbitzarira konetatu da! :)"
        elif(type=='left'):
            msg = user+" zerbitzaritik deskonetatu da :("

        masto(msg)
        tele(msg)

def masto(msg):
    mastodon = Mastodon(
        access_token = sys.path[0]+"/mastodon.credentials",
        api_base_url = 'https://botsin.space'
    )
    msg = msg + "\n#minecraft\nmc.zital.freemyip.com"
    mastodon.status_post(msg, visibility='public')

def tele(msg):
    token   = readFile(sys.path[0]+"/telegram.credentials").strip()
    channel = readFile(sys.path[0]+"/telegram.channel").strip()
    bot     = Bot(token=token)
    bot.send_message(chat_id=channel, text=msg)

def readFile(path):
    with open(path, 'r') as file:
        content = file.read()
    return content
    

#readLog(file)
tele('adasd')
