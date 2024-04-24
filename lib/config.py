#!/usr/bin/env python3

import os
import json

config_file_path = os.path.join(os.path.dirname(__file__), '../var/config.json')

def load():
    with open(config_file_path, "r") as f:
        data = json.load(f)
        return data

def save(data):
    with open(config_file_path, "w") as f:
        json_string = json.dumps(data, indent=4)
        f.write(json_string)