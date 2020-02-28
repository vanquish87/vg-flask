# send new user a message to persue fresher course to get multibagger mindset
#! /usr/bin/python3
import os, sys
# tells python the starting point of this project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), '..')))

from vg import db, app
from user.models import User, Cron
import datetime
from user.email_sms import send_sms


def fresher_course():
    users = User.query.order_by(User.registered_on.desc())
    time_now = datetime.datetime.utcnow()
    fresh_notice = 0
    
    for user in users:
        # msg_time will set the day to send him sms after last_seen_utc + 3 days
        msg_time = user.registered_on + datetime.timedelta(days=3)
        
        # exactly 3 din baad 1 msg only, 1st condition, 2nd condition so that woh roz msg na kare
        if time_now - msg_time < datetime.timedelta(days=1) and time_now - msg_time > datetime.timedelta(days=0):
            message="Gm %s, dost checkout the 'Secret Jugaad To Identify Multibaggers' course here : https://goo.gl/cB5Lti . Approved by thousands of VG." % user.fullname.title()
            
            cron_exist = Cron.query.filter_by(user_id=user.id, message=message).first()
            if cron_exist is None and user.mobile_ind is not None :
                send_sms(user.mobile_ind, message)
            
                if app.config["SEND_SMS"] == True:
                        sms_sent = True
                else:
                    sms_sent = False
                # to save activity in db
                purpose = "Fresher course notice"
                
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
    print('fresher_course is working')


fresher_course()