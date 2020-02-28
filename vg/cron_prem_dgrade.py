# notify premium member got converted into normal after expiry if any
# convert premium member into normal at expiry automatically
#! /usr/bin/python3
import os, sys
# tells python the starting point of this project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), '..')))

from vg import db, app
from user.models import User, Cron
import datetime
from user.email_sms import send_sms


def premium_downgrade():
    users = User.query.filter_by(is_premium=True).order_by(User.registered_on.desc())
    time_now = datetime.datetime.utcnow()
    
    for user in users:
        if time_now - user.premium_expiry_on > datetime.timedelta(days=0) and time_now - user.premium_expiry_on < datetime.timedelta(days=1):
            user.is_premium = 0
            db.session.commit()
            
            message="Hi %s, Dost your premium membership has expired n you are downgraded to normal account." % user.fullname.title()
            
            cron_exist = Cron.query.filter_by(user_id=user.id, message=message).first()
            if cron_exist is None and user.mobile_ind is not None :
                send_sms(user.mobile_ind, message)
            
                if app.config["SEND_SMS"] == True:
                        sms_sent = True
                else:
                    sms_sent = False
                    
                # to save activity in db
                purpose = "Premium Expired"
                
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
    
    print('premium_downgrade is working')
    
premium_downgrade()