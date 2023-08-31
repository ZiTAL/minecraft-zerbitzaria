# minecraft zerbitzaria

mc.zital.freeemyip.com

https://mc.zital.freeemyip.com

# minecraft bezeroa instalatzeko gida

https://peertube.eus/w/cinFjM6vWB5LgEJbcomjND

# download
```
mkdir /home/projects/mc
cd /home/projects/mc
wget https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar
mv server.jar server.1.20.1.jar
```

```
apt-get install openjdk-19-jre-headless
```

# server
**/etc/systemd/system/minecraft.service**
```
[Unit]
Description=Minecraft Server
After=network.target

[Service]
WorkingDirectory=/home/projects/mc
User=pi
Group=pi
Restart=on-failure
RestartSec=5
ExecStart=/usr/bin/java -Xms1G -Xmx2G -jar /home/projects/mc/server.1.20.1.jar nogui

[Install]
WantedBy=multi-user.target
```
```
systemctl enable minecraft.service
systemctl start minecraft.service
systemctl status minecraft.service

```

# bot
```
pip3 install -U Mastodon.py
```

**/etc/systemd/system/minecraft-bot.service**
```
[Unit]
Description=Minecraft Server Bot
After=network.target

[Service]
WorkingDirectory=/home/projects/mc/minecraft-zerbitzaria/scripts/bot
User=pi
Group=pi
Restart=on-failure
RestartSec=5
ExecStart=/usr/bin/python3 /home/projects/mc/minecraft-zerbitzaria/scripts/bot/bot.py

[Install]
WantedBy=multi-user.target
```
```
systemctl enable minecraft-bot.service
systemctl start minecraft-bot.service
systemctl status minecraft-bot.service

```

# mastodonen kredentzialak lortzeko python script-a
```
from mastodon import Mastodon
Mastodon.create_app('app_name', scopes=['read', 'write'], api_base_url="https://botsin.space")
api = Mastodon("code01", "code02", api_base_url="https://botsin.space")
api.log_in("email", "passwd", scopes=["read", "write"])
```

# telegram bot-a sortzeko gida

https://www.teleme.io/articles/create_your_own_telegram_bot?hl=en

# telegram kanala sortzeko gida

https://techpp.com/2022/01/08/how-to-create-telegram-channel-guide/

# telegram kanalaren ID-a lortzeko gida

**@getidsbot** telegram erabiltzaileari birbidali beharko diozu zure kanaleko mezuren bat

**Kanala sortzean aurretiz sortu dugun BOT-a sartu beharko dugu Admin modura.**

Behin hauek biak sortu eta gero **telegram.credentials** fitxategian API-aren TOKEN-a sartuko dugu, eta **telegram.channel** fitxategian kanalaren ID-a sortuko dugu "-" aurrizkiarekin, adibidez: **-1234567890123**

# web server

**/etc/nginx/sites-enabled/mc.conf**
```
server {
        include     /etc/nginx/vhost.conf.d/*.conf;

        server_name mc.zital.freemyip.com mc.opi5;
        root        /home/projects/mc/minecraft-zerbitzaria/scripts/server/;

        error_log   /var/log/nginx/mc-error.log error;
        access_log  /var/log/nginx/mc-access.log;

        # PHP-FPM configuration
        location ~ \.php$ {
                fastcgi_pass unix:/run/php/php8.1-fpm.sock;
                fastcgi_index index.php;
                include fastcgi_params;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        }

        location / {
                index index.php;
                try_files $uri $uri/ /index.php?$args;
        }
}
```

# Administratzaileak
**/home/projects/mc/ops.json**
```
[
  {
    "uuid": "1234-1234-1234-1234-1234",
    "name": "arkkuso",
    "level": 4,
    "bypassesPlayerLimit": false
  },
  {
    "uuid": "1234-1234-1234-1234-1234",
    "name": "zitalko",
    "level": 4,
    "bypassesPlayerLimit": false
  }
]

```

# Jokoan bertan

Edonok lo eginez eguna egiteko aukera:
```
/gamerule playersSleepingPercentage 0
```