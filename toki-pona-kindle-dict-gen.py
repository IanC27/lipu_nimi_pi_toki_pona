from jinja2 import Environment, FileSystemLoader
import requests
import os
import subprocess
import json
import argparse
# shell for this code: https://code-maven.com/minimal-example-generating-html-with-python-jinja

# parse args for language
parser = argparse.ArgumentParser(description="create a Toki Pona dictionary mobu for use in kindles")
parser.add_argument("-l", "--lang", help="the short code for the output language of the dictionary, as listed in the linku data")
parser.add_argument("-h", "--help")

response = requests.get("https://lipu-linku.github.io/jasima/data.json")
linku = json.loads(response.content)

args = parser.parse_args()
if not args.lang:
    LANG_ID = "en"
else:
    LANG_ID = args.lang

if LANG_ID not in linku["languages"].keys():
    print("Language not recognized. Be sure to use the correct language code.")
    quit()


root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir) )
template = env.get_template("cover-template.html")

# create cover from template
# https://stackoverflow.com/questions/22181944/using-utf-8-characters-in-a-jinja2-template
filename = os.path.join(root, "dict-files", "cover.html")
with open(filename, 'wb') as fh:
    output = template.render(lang = linku["languages"][LANG_ID]["name_toki_pona"])
    fh.write(output.encode("utf-8"))

# create dictionary content from template
defs = {}
for word, data in linku["data"].items():
    if LANG_ID in data["def"]:
        defn = data["def"][LANG_ID]
    else:
        # TODO: This should probably be translated, but I don't know any language other than English
        defn = "No definition found in your language"
    defs[word] = bytes(defn, "utf-8").decode("utf-8", "ignore")

template = env.get_template("content-template.html")
filename = os.path.join(root, "dict-files", "content.html")
with open(filename, "wb") as fh:
    output = template.render(defs = defs)
    fh.write(output.encode("utf-8"))

# create opf file from template
template = env.get_template("book-template.opf")
filename = os.path.join(root, "dict-files", "tok-" + LANG_ID + ".opf")
with open(filename, "w") as fh:
    fh.write(template.render(
        lang_tp = linku["languages"][LANG_ID]["name_toki_pona"],
        lang_id = LANG_ID
    ))

# run kindlegen to create the mobi file using opf file
subprocess.run([os.path.join(root, "kindlegen.exe"), filename])