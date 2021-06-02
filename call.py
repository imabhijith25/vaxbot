import requests
import json
pincode = "695029"
date="03-06-2021"
print(date.isalpha())
resp = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}".format(pincode=pincode,date=date))
x = resp.json()



for i in x["sessions"]:
    print(i["name"])
    print(i["address"])
    print(i['available_capacity_dose1'])
    print(i['available_capacity_dose2'])