import requests
import json

response = requests.get("https://lipu-linku.github.io/jasima/data.json")
linku = json.loads(response.content)
# print(linku["data"]["a"]["def"]["en"])
LANG_TO = "en"


with open("tok-" + LANG_TO + ".txt", "w", encoding="utf-8") as outfile:
    for entry in linku["data"].values():
        #print(entry)
        line = "{}\t{}\t[{}]\n".format(entry["word"], entry["def"][LANG_TO], entry["book"])
        # IDK if i need to add \r for windows or not
        outfile.write(line)
    
