import sys
import subprocess
import re
from   time     import time
from   mastodon import Mastodon

dir  = sys.path[0]
file = dir + "/../../../logs/latest2.log"
wait = 1

def readLog(filename):
    start_time   = int(time())
    tail_process = subprocess.Popen(["tail", "-f", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

def masto(msg):
    mastodon = Mastodon(
        access_token = sys.path[0]+"/mastodon.credentials",
        api_base_url = 'https://botsin.space'
    )
    msg = msg + "\n#minecraft\nmc.zital.freemyip.com"
    mastodon.status_post(msg, visibility='public')

readLog(file)