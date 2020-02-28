# to notify premium members for expiry within 30 days 15 days 7 days 2 days 
#! /usr/bin/python3
import os, sys
# tells python the starting point of this project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), '..')))

from vg import db, app
from user.models import User, Cron
import datetime
from user.email_sms import send_sms


def premium_notice():
    users = User.query.filter_by(is_premium=True).order_by(User.registered_on.desc())
    time_now = datetime.datetime.utcnow()
    
    for user in users:
        
        # to give premium expiry notice on 30th day to expiry
        if user.premium_expiry_on - time_now < datetime.timedelta(days=31) and user.premium_expiry_on - time_now > datetime.timedelta(days=30):
            message="%s ji, ur premium membership is going to expire in 30 days, please renew here: https://goo.gl/S1eV2v to continue awesomeness. Carpe Diem \m/" % user.fullname.title()
            
            cron_exist = Cron.query.filter_by(user_id=user.id, message=message).first()
            if cron_exist is None and user.mobile_ind is not None :
                send_sms(user.mobile_ind, message)
            
                if app.config["SEND_SMS"] == True:
                        sms_sent = True
                else:
                    sms_sent = False
                    
                # to save activity in db
                purpose = "Premium Expiry 30"
                
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
                
                
        # to give premium expiry notice on 15th day to expiry
        elif user.premium_expiry_on - time_now < datetime.timedelta(days=16) and user.premium_expiry_on - time_now > datetime.timedelta(days=15):
            message="%s ji, ur premium membership is going to expire in 15 days, please renew here: https://goo.gl/S1eV2v to continue awesomeness. Carpe Diem \m/" % user.fullname.title()
            
            cron_exist = Cron.query.filter_by(user_id=user.id, message=message).first()
            if cron_exist is None and user.mobile_ind is not None :
                send_sms(user.mobile_ind, message)
            
                if app.config["SEND_SMS"] == True:
                        sms_sent = True
                else:
                    sms_sent = False
                
                # to save activity in db
                purpose = "Premium Expiry 15"
                
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
                
        
        # to give premium expiry notice on 7th day to expiry
        elif user.premium_expiry_on - time_now < datetime.timedelta(days=8) and user.premium_expiry_on - time_now > datetime.timedelta(days=7):
            message="%s ji, ur premium membership is going to expire in 7 days, please renew here: https://goo.gl/S1eV2v to continue awesomeness. Carpe Diem \m/" % user.fullname.title()
            
            cron_exist = Cron.query.filter_by(user_id=user.id, message=message).first()
            if cron_exist is None and user.mobile_ind is not None :
                send_sms(user.mobile_ind, message)
            
                if app.config["SEND_SMS"] == True:
                        sms_sent = True
                else:
                    sms_sent = False
                
                # to save activity in db
                purpose = "Premium Expiry 7"
                
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
        
        
        # to give premium expiry notice on 2th day to expiry
        elif user.premium_expiry_on - time_now < datetime.timedelta(days=3) and user.premium_expiry_on - time_now > datetime.timedelta(days=2):
            message="%s ji, ur premium membership is going to expire tomorrow, please renew here: https://goo.gl/S1eV2v to continue awesomeness. Carpe Diem \m/" % user.fullname.title()
            
            cron_exist = Cron.query.filter_by(user_id=user.id, message=message).first()
            if cron_exist is None and user.mobile_ind is not None :
                send_sms(user.mobile_ind, message)
            
                if app.config["SEND_SMS"] == True:
                        sms_sent = True
                else:
                    sms_sent = False
                    
                # to save activity in db
                purpose = "Premium Expiry 2"
                
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
        
    print('premium_notice is working')
    
premium_notice()