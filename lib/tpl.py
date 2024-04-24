import os
from jinja2 import Template

def build(template_name, data):
    template_path = os.path.join(os.path.dirname(__file__), '../var/', template_name)

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file '{template_name}' not found at '{template_path}'.")

    with open(template_path, 'r') as file:
        template_content = file.read()
    
    template = Template(template_content)
    return template.render(data=data)