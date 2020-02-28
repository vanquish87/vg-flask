# models are database operations in flask in MVC Pattern & called models

# db is instance of SQLAlchemy from __init__.py file
from vg import db

# for inseting utc date & time
import datetime 

# for creating a dababase with name of user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    mobile_ind = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(60))
    
    
    # DateTime is a SQLAlchemy method to support python internal datetimer
    # registered_on, corfimed, confirmed_on_utc for email verification purposes 
    registered_on = db.Column(db.DateTime, nullable=False)
    # confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_mobile = db.Column(db.Boolean, nullable=False, default=False)
    # confirmed_on_utc = db.Column(db.DateTime, nullable=True)
    
    
    # for paid customer using this flag as 0 or 1
    is_premium = db.Column(db.Boolean)
    
    #if user is a admin(author) for blog to edit create wagarah wagarah
    is_author = db.Column(db.Boolean)
    
    adv_course = db.Column(db.Boolean)
    
    last_seen_utc = db.Column(db.DateTime, nullable=False)
    
    premium_registered_on = db.Column(db.DateTime, nullable=True)
    
    premium_expiry_on = db.Column(db.DateTime, nullable=True)
    
    # One-to-Many Relationships by SQLAlchemy to lookup dynamically in multiple tables
    # backref is a simple way to also declare a new property on the 'Post' class.
    # lazy defines when SQLAlchemy will load the data from the database
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    
    # for reviews this one to many relationship
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    
    Invites = db.relationship('Invite', backref='user', lazy='dynamic')
    Meetups = db.relationship('Meetup', backref='user', lazy='dynamic')
    Crons = db.relationship('Cron', backref='user', lazy='dynamic')
    
    
    # for instance of user
    def __init__(self, fullname, mobile_ind, password, confirmed_mobile=False, email=None, is_premium=False, is_author=False, adv_course=False, premium_registered_on=None, premium_expiry_on=None):
        self.fullname = fullname
        self.email = email
        self.mobile_ind = mobile_ind
        self.password = password
        
        # prints time in UTC format and stores it
        self.registered_on = datetime.datetime.utcnow()
        # self.confirmed = confirmed
        self.confirmed_mobile = confirmed_mobile
        # self.confirmed_on_utc = confirmed_on_utc
        
        self.is_premium = is_premium
        self.is_author = is_author
        self.adv_course = adv_course
        
        self.last_seen_utc = datetime.datetime.utcnow()
        self.premium_registered_on = premium_registered_on
        self.premium_expiry_on = premium_expiry_on
        
    # for fetching object from shell this will be seen
    def __repr__(self):
        return '<Unique User is : %r>' % self.fullname
    

# For storing reviews of users
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    rating = db.Column(db.Integer)
    title = db.Column(db.String(100))
    review = db.Column(db.Text)
    review_on_utc = db.Column(db.DateTime, nullable=False)
    # 'live' variable to check if it is draft or live 
    live = db.Column(db.Boolean)
    
    def __init__(self, user, rating, title, review, review_on_utc=None, live=False):
        # to use 'User' class object directly using Foreign key
        # bit confused about this line though...???
        self.user_id = user.id
        if rating >= 5 or rating < 1:
            self.rating = 5
        else:
            self.rating = rating
            
        self.title = title
        self.review = review
        if review_on_utc is None :
            self.review_on_utc = datetime.datetime.utcnow()
        self.live = live
    
    def __repr__(self):
        return '<Title is : %r>' % self.title
        

# for storing invitation data
class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invitee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mobile_invited = db.Column(db.String(16))
    invite_code = db.Column(db.Text)
    short_url = db.Column(db.String(6), unique=True)
    invite_on_utc = db.Column(db.DateTime, nullable=False)
    # to check if invite was used or not
    used = db.Column(db.Boolean)
    
    def __init__(self, user, mobile_invited, invite_code, short_url, invite_on_utc=None, used=False):
        self.invitee_id = user.id
        self.mobile_invited = mobile_invited
        self.invite_code = invite_code
        self.short_url = short_url
        if invite_on_utc is None:
            self.invite_on_utc = datetime.datetime.utcnow()
        self.used = used
        

class Meetup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purpose = db.Column(db.String(100))
    registered_utc = db.Column(db.DateTime)
    payment_done = db.Column(db.Boolean)
    payment = db.Column(db.Integer)
    
    def __init__(self, user, purpose, payment_done=False, payment=None):
        self.user_id = user.id
        self.purpose = purpose
        self.registered_utc = datetime.datetime.utcnow()
        self.payment_done = payment_done
        self.payment = payment
    

# saving cron jobs
class Cron(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purpose = db.Column(db.String(100))
    message = db.Column(db.String(320))
    sms_sent = db.Column(db.Boolean)
    sent_utc = db.Column(db.DateTime)
    sms_delivered = db.Column(db.Boolean)
    
    def __init__(self, user, purpose, message, sms_sent=False, sms_delivered=False):
        self.user_id = user.id
        self.purpose = purpose
        self.message = message
        self.sms_sent = sms_sent
        self.sent_utc = datetime.datetime.utcnow()
        self.sms_delivered = sms_delivered