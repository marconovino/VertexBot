from flask import Flask
from flask_restful import Api, Resource
from db import Database

db = Database()

app = Flask(__name__)
api = Api(app)
versionsDict = {
            "0.0.1":"youtube.com", 
            "0.0.2":"you1tube.com"
           }

versionList = db.get_all_versions()
for x in versionList:
    currID = x["versionid"]
    currLink = x["versiondownload"]
    versionsDict.update({currID:currLink})
print(versionsDict)