import requests
import json
from lib import tools

class Session:
    def __init__(self, username, password, server, site):
        self.username = username
        self.password = password
        self.server = server
        self.site = site
        self.cookie = None

    def login(self):
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = requests.post(f"https://{self.server}/api/login", json=payload)
        self.cookie = response.cookies.get_dict()

    def createvoucher(self, quota, up, down, bytes, note, n, expire_number, expire_unit):
        if not self.cookie:
            self.login()  

        expire_unit = tools.ToUnifyTime(expire_unit)

        payload = {
            "note" : note,
            "n" : n,
            "expire_number" : expire_number,
            "expire_unit" : expire_unit,
            "cmd" : "create-voucher"
        }

        if bytes > 0:
            payload["bytes"] = bytes

        if quota > 0:
            payload["quota"] = quota

        if down > 0:
            payload["down"] = down

        if up > 0:
            payload["up"] = up

        response = requests.post(f"https://{self.server}/api/s/{self.site}/cmd/hotspot", json=payload, cookies=self.cookie)
        obj = response.json()
        create_time = obj['data'][0]['create_time']

        response = requests.get(f"https://ui.sickl.at/api/s/{self.site}/stat/voucher?create_time={create_time}", cookies=self.cookie)
        obj = response.json()

        return obj['data'][0]['code']