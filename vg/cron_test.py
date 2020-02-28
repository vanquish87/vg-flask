#! /usr/bin/python3
import requests

def send_sms(to_mobile, message):
    USERNAME='Jasmeet'
    PASSWORD='492761'
    SENDER_ID = 'VALGUY'
    requests.get('http://sms.thinkbuyget.com/api.php?username='+USERNAME+'&password='+PASSWORD+'&sender='+SENDER_ID+'&sendto=91'+to_mobile+'&message='+message+'')
    # http://sms.thinkbuyget.com/api.php?username=Jasmeet&password=492761
    

message = 'lets try it out'

# send_sms('9871012220', message)
print(message)



# SHELL=/bin/bash
# MAILTO=""
# */1 * * * * cd /home/vanq87/apps/vg && source venv/bin/activate && python3 cron_test.py >> /home/vanq87/apps/cronlog.txt 2>&1


# 0 1 * * * cd /home/vanq87/apps/vg && source venv/bin/activate && python3 cron_prem_dgrade.py >> /home/vanq87/apps/cronlog.txt 2>&1
# 0 2 * * * cd /home/vanq87/apps/vg && source venv/bin/activate && python3 cron_fresher.py >> /home/vanq87/apps/cronlog.txt 2>&1
# 0 3 * * * cd /home/vanq87/apps/vg && source venv/bin/activate && python3 cron_prem_notice.py >> /home/vanq87/apps/cronlog.txt 2>&1

# */10 1-2 * * * cd /home/vanq87/apps/vg && source venv/bin/activate && python3 cron_prem_dgrade.py >> /home/vanq87/apps/cronlog.txt 2>&1
# */10 2-3 * * * cd /home/vanq87/apps/vg && source venv/bin/activate && python3 cron_fresher.py >> /home/vanq87/apps/cronlog.txt 2>&1
# */10 3-4 * * * cd /home/vanq87/apps/vg && source venv/bin/activate && python3 cron_prem_notice.py >> /home/vanq87/apps/cronlog.txt 2>&1



# SHELL=/bin/bash crontab jobs (including errors) is sent through
# MAILTO=""o the user the crontab file belongs to (unless redirected).
# #
# # For example, you can run a backup of all your user accounts
# */10 1-2 * * * cd /home/gatola564/apps/vg && source venv/bin/activate && python3 cron_prem_dgrade.py >> /home/gatola564/apps/cronlog.txt 2>&1
# */10 2-3 * * * cd /home/gatola564/apps/vg && source venv/bin/activate && python3 cron_fresher.py >> /home/gatola564/apps/cronlog.txt 2>&1
# */10 3-4 * * * cd /home/gatola564/apps/vg && source venv/bin/activate && python3 cron_prem_notice.py >> /home/gatola564/apps/cronlog.txt 2>&1


# sudo grep CRON /var/log/syslog
# sudo crontab -e

# Cron every day at 6pm
# 0 18 * * * command to be executed

# “At every 10th minute past every hour from 6 through 8.”
# */10 6-8 * * *