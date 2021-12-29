from flask import Flask
from flask_restful import Api, Resource
from db import Database
import asyncio

db = Database()
asyncio.run(db.setup())
app = Flask(__name__)
api = Api(app)
versionsDict = {
            "0.0.1":"youtube.com", 
            "0.0.2":"you1tube.com"
           }

loop = asyncio.get_event_loop()
versionList = asyncio.run(db.get_all_versions())

for x in versionList:
    currID = x["versionid"]
    currLink = x["versiondownload"]
    versionsDict.update({currID:currLink})
print(versionsDict)

class Versions(Resource):
    def get(self, versionid):
        return versionsDict[versionid]

api.add_resource(Versions, "/versions/<string:versionid>")
if __name__ == "__main__":
    app.run(debug=False)
