from flask_pymongo import pymongo
import requests
connectionurl = "mongodb+srv://test:test@cluster0.9xteb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client  = pymongo.MongoClient(connectionurl)
db = client.get_database('botbase')

point = db.states
st = db.stateid

#import db file, db.point.insert()
def getstate(msgid):
    x = point.find_one({"msgid":msgid})
    if(x is None):
        point.insert({"msgid":msgid, "state":"start"})
        return "start"
    else:
        return x["state"]

def setstateid(msgid,val):
    x = point.find_one({"msgid":msgid})
    if(x is not None):
        point.update_one({"msgid":msgid} ,
        {
            '$set':{
                'stateid':val

            }
        },upsert=False)
        return True
#setstateid(633111810,"17")
def getstateid(msgid):
    x= point.find_one({"msgid":msgid})
    if x is not None:
        return x["stateid"]
    else:
        return None
#print(getstateid(633111810))
def setdistrictid(msgid,val):
    x = point.find_one({"msgid":msgid})
    if(x is not None):
        point.update_one({"msgid":msgid} ,
        {
            '$set':{
                'distid':val

            }
        },upsert=False)
        return True

#setdistrictid(633111810,209)
def getdistid(msgid):
    x= point.find_one({"msgid":msgid})
    if x is not None:
        return x["distid"]
    else:
        return None
# print(getdistid(633111810))
def setstate(msgid,stateval):
    x = point.find_one({"msgid":msgid})
    if(x is not None):
        point.update_one({"msgid":msgid} ,
        {
            '$set':{
                'state':stateval

            }
        },upsert=False)
        return True
def findstateid(text):
    x = st.find_one({"state_name":text.lower()})
    if x is not None:
        return x["state_id"]
    else:
        return False


def getdistrict(ids,dname):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{ids}".format(ids=ids)
    diction = resp.json()
    li = diction["districts"]
    if len(li) != 0:
        for i in li:
            if(i["district_name"].lower() == dname):
                return i["district_id"]
                
    return False
    


# o = getdistrict("17","Kollam")
# print(o)
# print(o)

# statess=[{'state_id': 1, 'state_name': 'andaman and nicobar islands'}, {'state_id': 2, 'state_name': 'andhra pradesh'}, {'state_id': 3, 'state_name': 'arunachal pradesh'}, {'state_id': 4, 'state_name': 'assam'}, {'state_id': 5, 'state_name': 'bihar'}, {'state_id': 6, 'state_name': 'chandigarh'}, {'state_id': 7, 'state_name': 'chhattisgarh'}, {'state_id': 8, 'state_name': 'dadra and nagar haveli'}, {'state_id': 37, 'state_name': 'daman and diu'}, {'state_id': 9, 'state_name': 'delhi'}, {'state_id': 10, 'state_name': 'goa'}, {'state_id': 11, 'state_name': 'gujarat'}, {'state_id': 12, 'state_name': 'haryana'}, {'state_id': 13, 'state_name': 'himachal pradesh'}, {'state_id': 14, 'state_name': 'jammu and kashmir'}, {'state_id': 15, 'state_name': 'jharkhand'}, {'state_id': 16, 'state_name': 'karnataka'}, {'state_id': 17, 'state_name': 'kerala'}, {'state_id': 18, 'state_name': 'ladakh'}, {'state_id': 19, 'state_name': 'lakshadweep'}, {'state_id': 20, 'state_name': 'madhya pradesh'}, {'state_id': 21, 'state_name': 'maharashtra'}, {'state_id': 22, 'state_name': 'manipur'}, {'state_id': 23, 'state_name': 'meghalaya'}, {'state_id': 24, 'state_name': 'mizoram'}, {'state_id': 25, 'state_name': 'nagaland'}, {'state_id': 26, 'state_name': 'odisha'}, {'state_id': 27, 'state_name': 'puducherry'}, {'state_id': 28, 'state_name': 'punjab'}, {'state_id': 29, 'state_name': 'rajasthan'}, {'state_id': 30, 'state_name': 'sikkim'}, {'state_id': 31, 'state_name': 'tamil nadu'}, {'state_id': 32, 'state_name': 'telangana'}, {'state_id': 33, 'state_name': 'tripura'}, {'state_id': 34, 'state_name': 'uttar pradesh'}, {'state_id': 35, 'state_name': 'uttarakhand'}, {'state_id': 36, 'state_name': 'west bengal'}]

# # for i in statess:
# #     print(i)

# def gomap():
#     for i in statess:
#         st.insert_one(i)
# gomap()
