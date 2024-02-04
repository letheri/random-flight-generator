import pymongo
import json
from pymongo import InsertOne

client = pymongo.MongoClient('mongodb+srv://[USER]:[PASS]@cluster0.ijzxz4o.mongodb.net/?retryWrites=true&w=majority')
db = client.FlightSearch
collection = db.airlines
requesting = []

with open(r"airlines.json") as f:
    for jsonObj in f:
        myDict = json.loads(jsonObj)
        for i in myDict:
            requesting.append(InsertOne(i))

result = collection.bulk_write(requesting)
client.close()