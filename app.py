from flask import Flask
from flask_restful import Api, Resource
import psycopg2
import os

app = Flask(__name__)
api = Api(app)
versionList = []
versionsDict = {}
def updateDictionary():
    conn = psycopg2.connect(database=os.getenv('database'), user =os.getenv('user'), password = os.getenv('password'), host = os.getenv('host'), port = "5432")
    global versionsDict
    global versionList
    cur = conn.cursor()
    cur.execute("SELECT * FROM Versions")
    rows = cur.fetchall()
    for row in rows:
        currID = row[0]
        currLink = row[1]
        versionList.append(currID)
        versionsDict.update({currID:currLink})
    print(versionsDict)
    conn.close()

class GetVersion(Resource):
    def get(self, versionid):
        global versionsDict
        global versionList
        updateDictionary()
        if versionid not in versionList:
            return {"Error":"Invalid ID"}
        else:
            return versionsDict[versionid]

class ParseVersions(Resource):
    def get(self):
        global versionsDict
        global versionList
        updateDictionary()
        return versionsDict
        

api.add_resource(GetVersion, "/GetVersion/<string:versionid>")
api.add_resource(ParseVersions, "/ParseVersions")
if __name__ == "__main__":
    app.run(debug=False)
