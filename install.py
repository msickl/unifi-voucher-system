#!/usr/bin/env python3

import subprocess
from lib import config
from lib import tpl

cfg = config.load()

content = tpl.build('voucher.timer.tpl', cfg['timer'])
with open('etc/voucher.timer', "w") as f:
    f.write(content)

print("Create a symbolic link and configure the systemd service")
subprocess.run('ln -s /opt/voucher/etc/voucher.service /etc/systemd/system/', shell=True)
subprocess.run('ln -s /opt/voucher/etc/voucher.timer /etc/systemd/system/', shell=True)

subprocess.run('systemctl enable voucher.timer', shell=True)
subprocess.run('systemctl daemon-reload', shell=True)
subprocess.run('systemctl start voucher.timer', shell=True)