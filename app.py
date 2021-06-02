import telegram
from flask import Flask,request,session
from flask_sqlalchemy import SQLAlchemy
import requests 




app = Flask(__name__)
app.secret_key = "23nsdufsdsdsd"
key  = "1816007527:AAFrqEKhchPrExI2Ls1TI2GZZKUwJqBItkA"
bot = telegram.Bot(token=key)
@app.route("/")
def index():
    return "joii"

@app.route("/{}".format(key),methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    session["info"] = {
            "username" : update.message.chat.first_name,
   "text" : update.message.text,
    "chat_id" : update.message.chat.id,
    "msg_id" : update.message.message_id,

    }
    
    print("msg id",session["info"]["msg_id"]," chatid ",session["info"]["chat_id"], " " , session["info"]["username"])

    if(session["info"]["text"] == "/start"):
        welcometext = "Hi, {username}. Welcome to VaxBot. You can use this bot to check if Covid-19 vaccination is available in your area. Please Choose from the following options ".format(username=session["info"]["username"])
        custom_keyboard = [['Search By Pincode'],['Search By District']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=session["info"]["chat_id"],text=welcometext,reply_to_message_id=session["info"]["msg_id"],reply_markup=reply_markup)


    if(session["info"]["text"] == "Search By Pincode"):
        #change statecounter to pin
        pintext = "Enter your pincode and the date on which you would like to get vaccinated.\nThe format should be: pin pincode <space> DD-MM-YYYY \nEg: 110110 31-03-2021 "
   

        bot.sendMessage(chat_id=session["info"]["chat_id"],text=pintext,reply_to_message_id=session["info"]["msg_id"])

    return "done"


@app.route("/setwebhook/",methods=["GET","POST"])
def setwebhook():
    url = "https://f1946ab753ff.ngrok.io/"
    s = bot.setWebhook("{url}{key}".format(url=url,key=key))
  
    if s:
        return "Success"
    else:
        return "fail"
if __name__ == '__main__':
   app.run(debug=True)
