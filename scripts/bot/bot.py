#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip3 install -U Mastodon.py
# pip3 install -U requests

import sys
import subprocess
import re
import requests
from   time     import time
from   mastodon import Mastodon

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

    # [23:44:33] [Server thread/INFO]: [floodgate] Floodgate player logged in as .zitalko joined (UUID: 00000000-0000-0000-0000-000000000000)
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+\[floodgate\]", line, re.IGNORECASE)
    if(m):
        return False

    # [16:11:29] [Server thread/INFO]: arkkuso joined the game
    # [16:11:29] [Server thread/INFO]: arkkuso left the game
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+(.*?)\s+(joined|left)", line, re.IGNORECASE)
    if(m):
        user = m.group(1)
        type = m.group(2)

        if(type=='joined'):
            msg = " zerbitzarira konektatu da!"
        elif(type=='left'):
            msg = " zerbitzaritik deskonektatu da..."

        publish(user, msg)
        return True

    # [12:31:45] [Server thread/INFO]: .ARRUARTEGAMER was slain by Zombie
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+(.*?)\s+(was slain by)\s+(.*?)\s*$", line, re.IGNORECASE)
    if(m):
        user = m.group(1)
        enem = m.group(3)
        msg  = ", "+enem+" batek erahil du!"
        publish(user, msg)
        return True

    # [12:35:32] [Server thread/INFO]: .ARRUARTEGAMER fell from a high place
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+(.*?)\s+fell from a high place", line, re.IGNORECASE)
    if(m):
        user = m.group(1)
        msg  = " leku altu batetik erori da, eta kriston zartakoa hartu du!"
        publish(user, msg)
        return True        
    
    # [12:41:43] [Server thread/INFO]: .ARRUARTEGAMER has made the advancement [Suit Up]
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+(.*?)\s+has made the advancement \[(.*?)\]", line, re.IGNORECASE)
    if(m):
        user = m.group(1)
        adva = m.group(2)
        msg  = "-(e)k "+adva+" aurrerapena lortu du!"
        publish(user, msg)
        return True
        
    # [19:09:28] [Server thread/INFO]: ARRUARTE was shot by Pillager
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+(.*?)\s+was shot by\s+(.*?)$", line, re.IGNORECASE)
    if(m):
        user = m.group(1)
        enem = m.group(2)
        msg  = "-(e)ri "+enem+"-(e)k tiroa eman dio!"
        publish(user, msg)
        return True

    # [16:09:50] [Server thread/INFO]: .Dariusin16 tried to swim in lava
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+(.*?)\s+tried to swim in lava$", line, re.IGNORECASE)
    if(m):
        user = m.group(1)
        enem = m.group(2)
        msg  = " laban igeri egiten saiatu da..."
        publish(user, msg)
        return True

    # [16:06:22] [Server thread/INFO]: .Dariusin16 was doomed to fall by Enderman
    m = re.search(r"^\[[0-9]{2}:[0-9]{2}:[0-9]{2}\]\s+\[Server\sthread\/INFO\]:\s+(.*?)\s+was doomed to fall by\s+(.*?)$", line, re.IGNORECASE)                                
    if(m):
        user = m.group(1)
        enem = m.group(2)
        msg  = " erortzera kondenatu zuen "+enem+"-(e)k"
        publish(user, msg)
        return True
    
def prepareUser(user):
    return re.sub(r'^\.+', r'', user)

def masto(user, msg):
    msg = user + msg + "\n#minecraft\nmc.zital.eus"
    mastodon = Mastodon(
        access_token = sys.path[0]+"/mastodon.credentials",
        api_base_url = 'https://botsin.space'
    )
    mastodon.status_post(msg, visibility='public')

def tele(user, msg):
    msg     = "*"+user+"*" + mdEscapeSpecialChars(msg)
    token   = readFile(sys.path[0]+"/telegram.credentials").strip()
    channel = readFile(sys.path[0]+"/telegram.channel").strip()
    requests.get("https://api.telegram.org/bot"+token+"/sendMessage", params={
      "chat_id":    channel,
      "text":       msg,
      "parse_mode": 'MarkdownV2'
    })

def mdEscapeSpecialChars(msg):
    special  = r'_*[]()~`>#+-=|{}.!'
    pattern  = r'([' + re.escape(special) + '])'
    replacer = lambda match: '\\' + match.group(1)
    output   = re.sub(pattern, replacer, msg)
    return output

def publish(user, msg):
    user = prepareUser(user)
    masto(user, msg)
    tele(user, msg)

def readFile(path):
    with open(path, 'r') as file:
        content = file.read()
    return content

readLog(file)