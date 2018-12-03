
import pprint

from pymongo import MongoClient
client = MongoClient('7.188.0.80', 37777)
db = client['Citrix']
collection = db['citrix']
coll = db.list_collection_names()
cursor = collection.find()

print(coll)




a=[]

for i in cursor:

    try:
        license_type = {'license_type': i['license_info']['license_type']}
        i.update (license_type)
    except Exception as e:
           pass
    try:
        local_license_server_hostid = {'local_license_server_hostid': i['license_info']['local_license_server_hostid']}
        i.update(local_license_server_hostid)
    except Exception as e:
        pass
    try:
        license_expiry = {'license_expiry': i['license_info']['license_expiry']}
        i.update(license_expiry)
    except Exception as e:
        pass
    try:
        max_bw = {'max_bw': i['license_info']['max_bw']}
        i.update(max_bw)
    except Exception as e:
        pass
    try:
        model = {'model': i['license_info']['model']}
        i.update(model)
    except Exception as e:
        pass
    try:
        state = {'state': i['license_info']['state']}
        i.update(state)
    except Exception as e:
        pass
    try:
        system_patform = {'system_patform': i['license_info']['system_patform']}
        i.update(system_patform)
    except Exception as e:
        pass
    i.pop('license_info', None)

    a.append(i)
    print (len(a))

for x in range(0, len(a)):
    print(x)



