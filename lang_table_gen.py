from jinja2 import Environment, FileSystemLoader
import requests
import os
import json

response = requests.get("https://lipu-linku.github.io/jasima/data.json")
linku = json.loads(response.content)

# load template
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir))
template = env.get_template("language-table-template.html")

# create document
filename = os.path.join(root, "supported-languages.html")
with open(filename, 'wb') as fh:
    output = template.render(langs = linku["languages"])
    fh.write(output.encode("utf-8"))