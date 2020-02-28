from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# to use Migrate library to update databases & tables
from flask.ext.migrate import Migrate

# To initiate flask_uploads in our app
from flask_uploads.uploads import UploadSet, configure_uploads, IMAGES

# The Flask-Mail extension provides a simple interface to set up SMTP with 
# your Flask application and to send messages from your views and scripts.
from flask.ext.mail import Mail

# google recaptcha
from flask_recaptcha import ReCaptcha

# creating a instance of Flask as app
app = Flask(__name__)

# external settings.py file so that we can make changes while in devlopment or live servers
# this config is from Flask and from_object is a module for doing it
app.config.from_object('settings')

recaptcha = ReCaptcha(app=app)
# app.config.from_object(__name__)
recaptcha.get_code()


# create a object of SQLAlchemy with passing app as argument through it
db = SQLAlchemy(app)

# migrations
migrate = Migrate(app, db)




# for uploading images using flask_upload
upload_images_post = UploadSet('posts', IMAGES)
configure_uploads(app, upload_images_post)

# for setting up mail
mail = Mail()
mail.init_app(app)

# views are controller (which has to route) in flask in MVC Pattern
from website import views, views_admin, views_login
from user import views
from mrbull import views