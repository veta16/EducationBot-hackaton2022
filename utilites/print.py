import json

import sys


with open("import_data.json", "r") as file:
  file = json.load(file)

print(file['courses'][sys.argv[1]]['progress'][sys.argv[2]])