from model.firebase import db
import json


with open("import_data.json", "r") as file:
  db.reference('/').set(json.load(file))