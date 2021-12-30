from flask import Flask
from flask_restful import Api, Resource
import psycopg2
import os

conn = psycopg2.connect(database=os.getenv('database'), user =os.getenv('user'), password = os.getenv('password'), host = os.getenv('host'), port = "5432")
print("Opened database successfully")
cur = conn.cursor()

app = Flask(__name__)
api = Api(app)
versionList = []
versionsDict = {
            "0.0.1":"youtube.com", 
            "0.0.2":"you1tube.com"
               }
def updateDictionary():
    global versionsDict
    global versionList
    cur.execute("SELECT * FROM Versions")
    rows = cur.fetchall()
    for row in rows:
        currID = row[0]
        currLink = row[1]
        versionList.append(currID)
        versionsDict.update({currID:currLink})
    print(versionsDict)
    conn.close()

class Versions(Resource):
    def get(self, versionid):
        global versionsDict
        global versionList
        updateDictionary()
        if versionid not in versionList:
            return {"Error":"Invalid ID"}
        else:
            return versionsDict[versionid]

api.add_resource(Versions, "/versions/<string:versionid>")
if __name__ == "__main__":
    app.run(debug=False)
