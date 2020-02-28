# Let’s create a basic function for sending emails with a little help from Flask-Mail
# which is already installed and setup in project/__init__.py.
from flask.ext.mail import Message
from flask import flash
from vg import app, mail
import requests


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
    
# we simply need to pass a list of recipients, a subject, and a template.
# We’ll deal with the mail configuration settings in a bit.


# simple http api to send sms
# set bulk sms in advance so that we can choose from GET with list or without list (of 91 codes)
def send_sms(to_mobile, message, bulk=False):
    SENDER_ID = 'VALGUY'
    AUTHKEY = '171496AYGOQos4H599eace8'
    COUNTRY_CODE = '91'
    
    if app.config["SEND_SMS"] == True:
        if bulk == False:
            # this code needs mobile no. prefixed with 91 india code
            requests.get('http://my.msgwow.com/api/sendhttp.php?authkey='+AUTHKEY+'&mobiles=91'+to_mobile+'&message='+message+'&sender='+SENDER_ID+'&route=4&country='+COUNTRY_CODE+'')
        else:
            # without 91 code which will will added by in list beforehand        
            requests.get('http://my.msgwow.com/api/sendhttp.php?authkey='+AUTHKEY+'&mobiles='+to_mobile+'&message='+message+'&sender='+SENDER_ID+'&route=4&country='+COUNTRY_CODE+'')
    else:
        flash(to_mobile)
        flash(message)
    
    
    # USERNAME='Jasmeet'
    # PASSWORD='492761'
    # SENDER_ID = 'VALGUY'
    # # http://sms.thinkbuyget.com/api.php?username=Jasmeet&password=492761
    
    # if app.config["SEND_SMS"] == True:
    #     requests.get('http://sms.thinkbuyget.com/api.php?username='+USERNAME+'&password='+PASSWORD+'&sender='+SENDER_ID+'&sendto=91'+to_mobile+'&message='+message+'')
    # else:
    #     flash(to_mobile)
    #     flash(message)
    
# http://10seconds.in/pricing/ contact Rahul +91 9899338847 , 9999 273 424
# http://sms.thinkbuyget.com/api.php?username=Jasmeet&password=492761&sender=VALGUY&sendto=9867831373&message='Hitesh Patel ji, VGEX is rocked at 151% in April. What about u? Checkout latest holdings : https://goo.gl/s9XQ4C'&dlrUrl=http://www.valueguyz.com?logID=$logID$%26phNo=$phNO$%26result=$result$  