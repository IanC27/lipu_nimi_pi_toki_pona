from jinja2 import Environment, FileSystemLoader
import requests
import os
import subprocess
import json
import argparse
# code for deploying templates: https://code-maven.com/minimal-example-generating-html-with-python-jinja

# parse args for language
parser = argparse.ArgumentParser(description="create a Toki Pona dictionary mobi for use in kindles")
parser.add_argument("-a", "--all", help="compile dictionaries for all languages available", action="store_true")
parser.add_argument("lang", help="the short id for the output language of the dictionary, as listed in the linku data", default=["en"], nargs="*")
args = parser.parse_args()

#get the Linku
response = requests.get("https://lipu-linku.github.io/jasima/data.json")
linku = json.loads(response.content)

# set up
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir))

if args.all:
    languages = linku["languages"].keys()
else:
    languages = args.lang


for LANG_ID in languages:
    if LANG_ID not in linku["languages"].keys():
       print(f"Language id '{LANG_ID}' not recognized. run lang_table_gen.py and check supported-languages.html for valid language ids.")
       continue

    id_long = linku["languages"][LANG_ID]["id_long"]
     # create cover from template
    template = env.get_template("cover-template.html")
    filename = os.path.join(root, "dict-files", id_long, "cover.html")
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as fh:
        output = template.render(lang = linku["languages"][LANG_ID]["name_toki_pona"])
        # https://stackoverflow.com/questions/22181944/using-utf-8-characters-in-a-jinja2-template
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
    filename = os.path.join(root, "dict-files", id_long, "content.html")
    with open(filename, "wb") as fh:
        output = template.render(defs = defs)
        fh.write(output.encode("utf-8"))

    # create copyright/credits page
    template = env.get_template("copyright.html")
    filename = os.path.join(root, "dict-files", id_long, "copyright.html")
    with open(filename, "w") as fh:
        fh.write(template.render())

    # create opf file from template
    template = env.get_template("book-template.opf")
    filename = os.path.join(root, "dict-files", id_long, "tok-" + LANG_ID + ".opf")
    with open(filename, "w") as fh:
        fh.write(template.render(
            lang_tp = linku["languages"][LANG_ID]["name_toki_pona"],
            lang_id = LANG_ID
        ))

    # now compile the mobi file
    if (os.path.exists("kindlegen.exe")):
        subprocess.run(["kindlegen", filename])

