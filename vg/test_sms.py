# send new user a message to persue fresher course to get multibagger mindset
#! /usr/bin/python3
import os, sys
# tells python the starting point of this project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), '..')))

from vg import db, app
from user.models import User, Cron
import datetime
from user.email_sms import send_sms


def vgex_message():
    users = User.query.order_by(User.registered_on.desc())
    for user in users:
        message="%s ji, VGEX is rocked at 151%% in April. What about u? Checkout latest holdings : https://goo.gl/s9XQ4C" % user.fullname.title()
        cron_exist = Cron.query.filter_by(user_id=user.id, message=message).first()
        if cron_exist is None and user.mobile_ind is not None :
            send_sms(user.mobile_ind, message)
        
            if app.config["SEND_SMS"] == True:
                    sms_sent = True
            else:
                sms_sent = False
            # to save activity in db
            purpose = "VGEX Apr17 update"
            
            cron = Cron(user,
                        purpose,
                        message,
                        sms_sent)
            
            db.session.add(cron)
            db.session.flush()
            if cron.id:
                db.session.commit()
            else:
                db.session.rollback()
    print('vgex_message is working')
    
# vgex_message()

def premium_msg():
    users = User.query.order_by(User.registered_on.desc())
    numbers = 0
    for user in users:
        message="Dost,\nSale on Premium membership is LIVE\nGet it for 4999/Yr now:\nhttps://goo.gl/Q7dmqH\n\nRegards,\nJasmeet\n(SEBI regd.)"
        if user.is_premium == False and user.mobile_ind is not None:
            numbers = numbers + 1
            # send_sms(user.mobile_ind, message)
            
    print(numbers)
    print(message)

premium_msg()
            
            
            
            
            
            
            
            
            
            