
import pprint

from pymongo import MongoClient
client = MongoClient('7.188.0.80', 37777)
db = client['Citrix']
collection = db['Costs']
coll = db.list_collection_names()
cursor = collection.find()

print(coll)




a=[]

for i in cursor:
    pprint.pprint (i['Type'])


