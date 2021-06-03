import telegram
from flask import Flask,request,session
import db
import requests 




app = Flask(__name__)
app.secret_key = "23nsdufsdsdsd"
key  = "1816007527:AAFrqEKhchPrExI2Ls1TI2GZZKUwJqBItkA"

bot = telegram.Bot(token=key)







@app.route("/")
def index():

    # user = Users.query.delete()
    # db.session.commit()
    # print(user)
    return "hii"
@app.route("/{}".format(key),methods=["POST"])
def respond():

    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if(update is not None and(update.message is not None ) ):
        session["info"] = {

            "username" : update.message.chat.first_name,
            "text" : update.message.text,
            "chat_id" : update.message.chat.id,
            "msg_id" : update.message.message_id
    

            }
        print("msg id",session["info"]["msg_id"]," chatid ",session["info"]["chat_id"], " " , session["info"]["username"])
        if(session["info"]["text"] == "/start" ):
            db.setstate(session["info"]["chat_id"],"start")
            session["counter"]=0

        if(db.getstate(session["info"]["chat_id"]) == "start"):
            
            welcometext = "Hi, {username}. Welcome to VaxBot. You can use this bot to check if Covid-19 vaccination is available in your area. Please Choose from the following options ".format(username=session["info"]["username"])
            custom_keyboard = [['Search By Pincode'],['Search By State']]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,one_time_keyboard=True)
            y = bot.sendMessage(chat_id=session["info"]["chat_id"],text=welcometext,reply_to_message_id=session["info"]["msg_id"],reply_markup=reply_markup)
            session["counter"]=1
            if y:
                db.setstate(session["info"]["chat_id"],"check")

        elif(session["info"]["text"] == "Search By Pincode" and db.getstate(session["info"]["chat_id"]) == "check"):

            
            #change statecounter to pin
            pintext = "Enter your pincode and the date on which you would like to get vaccinated.\nThe format should be: pincode <space> DD-MM-YYYY \nEg: 110110 31-03-2021 "
    

            x = bot.sendMessage(chat_id=session["info"]["chat_id"],text=pintext,reply_to_message_id=session["info"]["msg_id"])
            if x:
                db.setstate(session["info"]["chat_id"] ,"pin")

        elif(session["info"]["text"] == "Search By State" and db.getstate(session["info"]["chat_id"]) == "check"):
            statetext = "Enter the name of your state"
            s = bot.sendMessage(chat_id=session["info"]["chat_id"],text=statetext,reply_to_message_id=session["info"]["msg_id"])
            if s:
                db.setstate(session["info"]["chat_id"] ,"state")

        
        elif((session["info"]["text"].isalpha() == True) and (db.getstate(session["info"]["chat_id"])  == "state")):
            stateid = db.findstateid(session["info"]["text"])
            
            if(stateid == False):
                bot.sendMessage(chat_id=session["info"]["chat_id"],text="Couldn't find state. There could be a problem with spelling. /start again")
            #send messge to enter district and set state to district 
            else:
                reptext = "Enter the name of your district in {statename}".format(statename = session["info"]["text"])
                db.setstateid(session["info"]["chat_id"] ,stateid)
                #print(session["stateid"])
                n = bot.sendMessage(chat_id=session["info"]["chat_id"],text=reptext,reply_to_message_id=session["info"]["msg_id"])
                if n:
                    db.setstate(session["info"]["chat_id"] ,"district")

        

        elif((session["info"]["text"].isalpha() == True) and (db.getstate(session["info"]["chat_id"])  == "district")):
            stval = db.getstateid(session["info"]["chat_id"])
            if(stval!=None):
                val = db.getdistrict(stval,session["info"]["text"].lower())
                print(val)
                if(val == False):
                    bot.sendMessage(chat_id=session["info"]["chat_id"],text="Wrong name. Must be a problem with spelling. /start again")

                else:
                    #ivde session["distid"] =val
                    db.setdistrictid(session["info"]["chat_id"],val)
                    datt = "Enter date on which you would like to get vaccinated.\nFormat DD-MM-YYYY\nEg: 02-02-2021"
                    k = bot.sendMessage(chat_id=session["info"]["chat_id"],text=datt)
                    if k:
                        db.setstate(session["info"]["chat_id"] ,"date")
                


        
        elif((session["info"]["text"].isalpha() == False) and (db.getstate(session["info"]["chat_id"])  == "date")):
        
            distid_d = db.getdistid(session["info"]["chat_id"])
            if(distid_d is not None):
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                resp1 = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={distid}&date={date}".format(distid=distid_d,date=session["info"]["text"]),headers=headers)
                j1 = resp1.json()
                print(resp1.status_code)
                if(j1 is not None):
                    for j in j1["sessions"]:
                        h1_name = j["name"]
                        h1_addr = j["address"] 
                        h1_cap1 = j["available_capacity_dose1"]  
                        h1_cap2 = j["available_capacity_dose2"]
                        total1 = j["available_capacity"]
                        det1 =   "{hos_name} \n{hos_adr} \nDose one Available:{hos_cap1} \nDose two Available:{hos_cap2}\nTotal Dose:{total1}".format(hos_name=h1_name,hos_adr = h1_addr,hos_cap1=h1_cap1, hos_cap2 = h1_cap2,total1=total1)
                        bot.sendMessage(chat_id=session["info"]["chat_id"],text=det1)
                else:
                    bot.sendMessage(chat_id=session["info"]["chat_id"],text="Cannot get data")

                continuetext1 = "would you like to coninue"
                custom_keyboard1 = [['Yes'],['No']]
                reply_markup1 = telegram.ReplyKeyboardMarkup(custom_keyboard1,one_time_keyboard=True)
                zss = bot.sendMessage(chat_id=session["info"]["chat_id"],text=continuetext1,reply_to_message_id=session["info"]["msg_id"],reply_markup=reply_markup1)
                if zss:
                    db.setstate(session["info"]["chat_id"],"continue")

        

        #handling pincode. check for getstate is pin only. and input value not none.
        elif((session["info"]["text"].isalpha() == False) and (db.getstate(session["info"]["chat_id"])  == "pin")):
            #handlepincode  
            print("wat")
            li = session["info"]["text"].split(" ")
            print(li)
            pincode = li[0]
            date = li[1]
            urli = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}".format(pincode=pincode,date=date)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            resp = requests.get(urli,headers =headers)
            
            print(resp.status_code)
            if(resp.status_code == 200):
                jsonified  = resp.json()
                for i in jsonified["sessions"]:
                    hos_name = i["name"]
                    hos_address = i["address"]
                    hos_cap1 = i['available_capacity_dose1']
                    hos_cap2 = i['available_capacity_dose2']
                    total = i['available_capacity']
                    details = "{hos_name} \n{hos_adr} \nDose one Available:{hos_cap1} \nDose two Available:{hos_cap2}\n Total Doses: {total}".format(hos_name=hos_name,hos_adr = hos_address,hos_cap1=hos_cap1, hos_cap2 = hos_cap2,total=total)
                    bot.sendMessage(chat_id=session["info"]["chat_id"],text=details)
            else:
                bot.sendMessage(chat_id=session["info"]["chat_id"],text="Cannot ger data")

            
            continuetext2 = "would you like to coninue"
            custom_keyboard2 = [['Yes'],['No']]
            reply_markup2 = telegram.ReplyKeyboardMarkup(custom_keyboard2,one_time_keyboard=True)
            z = bot.sendMessage(chat_id=session["info"]["chat_id"],text=continuetext2,reply_to_message_id=session["info"]["msg_id"],reply_markup=reply_markup2)
            if z:
                db.setstate(session["info"]["chat_id"],"continue")

        #handlesistrict

        elif((session["info"]["text"] == "Yes") and (db.getstate(session["info"]["chat_id"])  == "continue")):
            m = db.setstate(session["info"]["chat_id"],"start")
            if m:
                bot.sendMessage(chat_id=session["info"]["chat_id"],text="Good Choice!!",reply_to_message_id=session["info"]["msg_id"])
                bot.sendMessage(chat_id=session["info"]["chat_id"],text="Click /start to begin again",)
        

        elif((session["info"]["text"] == "No") and (db.getstate(session["info"]["chat_id"])  == "continue")):
            thankmessage="Thanks for using VaxBot. If you want to check again, just type in /start onto the textarea. :)"
            bot.sendMessage(chat_id=session["info"]["chat_id"],text=thankmessage,reply_to_message_id=session["info"]["msg_id"])   
        else:
            bot.sendMessage(chat_id=session["info"]["chat_id"],text="Invalid Command. Please /start again.",reply_to_message_id=session["info"]["msg_id"]) 

    return "done"


@app.route("/setwebhook/",methods=["GET","POST"])
def setwebhook():
    url = "https://vaxbotapp.herokuapp.com/"
    s = bot.setWebhook("{url}{key}".format(url=url,key=key))
  
    if s:
        return "Success"
    else:
        return "fail"
if __name__ == '__main__':
   app.run(debug=True)
