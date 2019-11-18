#! /usr/bin/python3
import os, sys
# tells python the starting point of this project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), '..')))

from vg import db, app
from user.models import User
from user.email_sms import send_sms
    

# creates string of mobiles ie, 9999666000, 9999666002 ...
def mobile_list():
    mobiles =  []
    users = User.query.order_by(User.registered_on.desc())
    for user in users:
        if user.mobile_ind:
            mobile_91 = "91"+str(user.mobile_ind)
            mobiles.append(mobile_91)
    string_mob = ','.join(mobiles)
    return string_mob
  
 
message = "Hi!\nsharukh kahn, Welcome to valueguyz.com.\nYou will be set free I promise\nJust keep up with the updates via SMSs\n\nJasmeet Singh\nSEBI Regd."
numbers = 0

mobile_list = mobile_list()
# for sending bulk sms set positional argument as True
# send_sms(mobile_list, message, bulk=True)
numbers = numbers + 1

print(mobile_list)
print(numbers)
print(message)
        