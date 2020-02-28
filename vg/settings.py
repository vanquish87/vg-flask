import os

# secret keys are used to encode sessions in Flask
# secret_key can be changed anytime database stored password are retrieved without problem
SECRET_KEY = '8B\xd5^\x10lv=/\x93K\x86`\xfaB>\x186\xa9i\xfe\xd5\xa9y'


# using os.urandom for email verification
SECURITY_PASSWORD_SALT = '\x92\xd1\xc3\xcb \x16$|\xdd*\xf8)\n\xf0\x0b\xca*\x0f\xce6S\xef\xe9\xd1'

RECAPTCHA_SITE_KEY = '6LfYeBgUAAAAAEWS2s5O0hwyBIzQIYEMRIKHDETN'
RECAPTCHA_SECRET_KEY = '6LfYeBgUAAAAACPE6RLXvyThjOFbQ_d80bDrrZMD'
# disabled recaptcha
RECAPTCHA_ENABLED = False

# DEBUG used in Development environment
DEBUG = True

# for sending sms via API http://10seconds.in/pricing/ contact Rahul +91 9899338847
SEND_SMS = False
# premium membership routes common variable
SALE_OPEN = False

# SQLAlchemy URI value to start doing things with databsase
DB_USERNAME = 'jasmeet87'
DB_PASSWORD = ''
WEBSITE_DATABASE_NAME = 'website'
DB_HOST = os.getenv('IP', '0.0.0.0')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, WEBSITE_DATABASE_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
# To supress warning on runserver --just to take kum space on shell
SQLALCHEMY_TRACK_MODIFICATIONS = True

# flask-upload settings for uploads ie, images
UPLOADS_DEFAULT_DEST = "/home/ubuntu/workspace/vg/static/images"

# prefix on the url for image link in jinja HTML template (flask-upload)
UPLOADS_DEFAULT_URL = '/static/images/'

 # mail settings
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_SERVER = 'smtp.zoho.com'
MAIL_PORT = 587

# zoho authentication
MAIL_USERNAME = 'valueguyz-admin@valueguyz.com'
MAIL_PASSWORD = 'code4ruby@feb14'

# mail accounts
MAIL_DEFAULT_SENDER = 'valueguyz-admin@valueguyz.com'


#instamojo stuff
API_KEY = "931abee575d7e62453f2a2cd1a0227c0"
AUTH_TOKEN = "aa0fd13351a622ba1e3c2acac4ec348b"
PRIV_SALT = "b7bbacc776c4876ec7d5de1f7118ce3b"
