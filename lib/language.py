#!/usr/bin/env python3

import os
import json
from jinja2 import Template

config_file_path = os.path.join(os.path.dirname(__file__), '../var/lang.json')

def load(client):
    with open(config_file_path, "r") as f:
        if client.get('lang'):
            print(f"Use language {client['lang']}")
            data = json.load(f)[client['lang']]
        else:
            data = json.load(f)['en-en']
            print(f"Use default language en-en")
    
    json_string = json.dumps(data)
    template = Template(json_string)
    json_string = template.render(client=client)

    data = json.loads(json_string)

    return data