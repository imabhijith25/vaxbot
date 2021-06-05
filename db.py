from flask_pymongo import pymongo
import requests
connectionurl = ""
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
    headers = {    'Accept':'text/html,application/xhtml+xml,application/xml',
                                'Accept-Encoding':'gzip, deflate',
                                'Accept-Charset':'ISO-8859-1',
                                'Origin':'https://www.cowin.gov.in',
                                'referer':'https://www.cowin.gov.in/',
                                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',}
    resp = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{ids}".format(ids=ids),headers=headers)
    print(resp.status_code)
    diction = resp.json()
    li = diction["districts"]
    if len(li) != 0:
        for i in li:
            if(i["district_name"].lower() == dname):
                return i["district_id"]
                
    return False
    


