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
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        if(update is not None):
            session["info"] = {

                "username" : update.message.chat.first_name,
                "text" : update.message.text,
                "chat_id" : update.message.chat.id,
                "msg_id" : update.message.message_id,

                }
            print("msg id",session["info"]["msg_id"]," chatid ",session["info"]["chat_id"], " " , session["info"]["username"])
            if(session["info"]["text"] == "/start" ):
                db.setstate(session["info"]["chat_id"],"start")

            if(db.getstate(session["info"]["chat_id"]) == "start"):
                
                welcometext = "Hi, {username}. Welcome to VaxBot. You can use this bot to check if Covid-19 vaccination is available in your area. Please Choose from the following options ".format(username=session["info"]["username"])
                custom_keyboard = [['Search By Pincode'],['Search By District']]
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,one_time_keyboard=True)
                y = bot.sendMessage(chat_id=session["info"]["chat_id"],text=welcometext,reply_to_message_id=session["info"]["msg_id"],reply_markup=reply_markup)
                if y:
                    db.setstate(session["info"]["chat_id"],"check")

            elif(session["info"]["text"] == "Search By Pincode" and db.getstate(session["info"]["chat_id"]) == "check"):
                
                #change statecounter to pin
                pintext = "Enter your pincode and the date on which you would like to get vaccinated.\nThe format should be: pincode <space> DD-MM-YYYY \nEg: 110110 31-03-2021 "
        

                x = bot.sendMessage(chat_id=session["info"]["chat_id"],text=pintext,reply_to_message_id=session["info"]["msg_id"])
                if x:
                    db.setstate(session["info"]["chat_id"] ,"pin")


            

            #handling pincode. check for getstate is pin only. and input value not none.
            elif((session["info"]["text"].isalpha() == False) and (db.getstate(session["info"]["chat_id"])  == "pin")):
                #handlepincode  
                print("wat")
                li = session["info"]["text"].split(" ")
                print(li)
                pincode = li[0]
                date = li[1]
                resp = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}".format(pincode=pincode,date=date))
                jsonified = resp.json()
                
                for i in jsonified["sessions"]:
                    hos_name = i["name"]
                    hos_address = i["address"]
                    hos_cap1 = i['available_capacity_dose1']
                    hos_cap2 = i['available_capacity_dose2']
                    details = "{hos_name} \n{hos_adr} \nDose one Available:{hos_cap1} \nDose two Available:{hos_cap2}".format(hos_name=hos_name,hos_adr = hos_address,hos_cap1=hos_cap1, hos_cap2 = hos_cap2)
                    bot.sendMessage(chat_id=session["info"]["chat_id"],text=details)

                continuetext = "would you like to coninue"
                custom_keyboard = [['Yes'],['No']]
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,one_time_keyboard=True)
                z = bot.sendMessage(chat_id=session["info"]["chat_id"],text=continuetext,reply_to_message_id=session["info"]["msg_id"],reply_markup=reply_markup)
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
    except:
        print("I don't know")
    return "done"


@app.route("/setwebhook/",methods=["GET","POST"])
def setwebhook():
    url = "https://e97a43185b82.ngrok.io/"
    s = bot.setWebhook("{url}{key}".format(url=url,key=key))
  
    if s:
        return "Success"
    else:
        return "fail"
if __name__ == '__main__':
   app.run(debug=True)
