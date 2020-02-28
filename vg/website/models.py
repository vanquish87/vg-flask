# models are database operations in flask in MVC Pattern & called models

# db is instance of SQLAlchemy from __init__.py file
# uploaded_images_post is a intance of flask_upload for uploading images
from vg import db, upload_images_post

# for inseting utc date & time
from datetime import datetime

# for creating a dababase with name of blog for posts etc.
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_name = db.Column(db.String(80), unique=True)
    
    # Flask-Admin has limited support for models with multiple primary keys.
    # It only covers specific case when all but one primary keys are foreign keys to another model.
    # it tells here that this particular id in User (used 'user': IDK ? ) to tell Blog it is an admin
    admin = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # One-to-Many Relationships by SQLAlchemy to lookup dynamically in multiple tables
    # backref is a simple way to also declare a new property on the 'Post' class.
    # lazy defines when SQLAlchemy will load the data from the database
    posts = db.relationship('Post', backref='blog', lazy='dynamic')
    
    # for instance of user
    def __init__(self, blog_name, admin):
        self.blog_name = blog_name
        self.admin = admin
        
    # for fetching object from shell this will be seen
    def __repr__(self):
        return '<Blog name is : %r>' % self.blog_name
    
    
# for creating a dababase with for posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    image = db.Column(db.String(255))
    
    title = db.Column(db.String(120))
    
    # slug is basically the url: jo actually dikhta hia
    # note that i used unique 190 not 255 because of some shitty error in db migrate as '1071, 'Specified key was too long; max key length is 767 bytes''
    slug = db.Column(db.String(190), unique=True)
    
    # description will be used to provide snippets of post when called from category pages ie, value pick
    description = db.Column(db.String(800))
    
    # DateTime is a SQLAlchemy method to support python internal datetime
    publish_date_utc = db.Column(db.DateTime)
    
    # 'live' variable to check if it is draft or live 
    live = db.Column(db.Boolean)
    
    # post category ie, value pick, mkt. commentary etc
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # One-to-Many Relationships by SQLAlchemy to lookup dynamically in multiple tables
    # backref is a simple way to also declare a new property on the 'Category' class.
    # lazy defines when SQLAlchemy will load the data from the database
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))
    
    
    meta_og_tags_title = db.Column(db.Text)
    
    # custom_css_files = db.Column(db.Text)
    
    image_n_video = db.Column(db.Text)
    
    full_link = db.Column(db.Text)
    
    body_intro = db.Column(db.Text)
    
    table_summary = db.Column(db.Text)
    
    body_details_website_box = db.Column(db.Text)
    
    quality_value_boxes = db.Column(db.Text)
    
    annual_report_table = db.Column(db.Text)
    
    premium_content = db.Column(db.Boolean)
    
    read_time = db.Column(db.Integer)
    
    simple_content = db.Column(db.Boolean)
    
    
    @property
    def imgsrc(self):
        return upload_images_post.url(self.image)
    
    
    def __init__(self, blog, user, title, category, slug, description, meta_og_tags_title, image_n_video, full_link, body_intro, table_summary,  body_details_website_box, read_time, quality_value_boxes=None, annual_report_table=None, image=None, publish_date_utc=None, live=True, premium_content=False, simple_content=False):
        
        # to use 'Blog' class object directly using Foreign key
        # bit confused about this line though...???
        self.blog_id = blog.id
        self.user_id = user.id
        self.title = title
        self.category_id = category.id
        self.slug = slug
        self.description = description
        
        
        self.meta_og_tags_title = meta_og_tags_title
        self.image_n_video = image_n_video
        
        self.full_link = full_link
        
        self.body_intro = body_intro
        self.table_summary = table_summary
        self.body_details_website_box = body_details_website_box
        
        self.read_time = read_time
        
        if quality_value_boxes:
            self.quality_value_boxes = quality_value_boxes
            
        if annual_report_table:
            self.annual_report_table = annual_report_table
        
        
        self.image = image
        # prints time in UTC format and stores it
        if publish_date_utc is None:
            self.publish_date_utc = datetime.utcnow()
        else:
            self.publish_date_utc = datetime.utcnow()
            
        self.live = live
        self.premium_content = premium_content
        self.simple_content = simple_content

    
    # for fetching object from shell this will be seen
    def __repr__(self):
        return '<Post is : %r>' % self.title
        
# for creating a dababase for category
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    def __init__(self, name):
        self.name = name
        
    # for fetching object from shell this will be seen
    def __repr__(self):
        return self.name
        
        
# for storing lectures in db
class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lecture_no = db.Column(db.Integer)
    section = db.Column(db.String(80))
    title = db.Column(db.String(80))
    duration = db.Column(db.String(6))
    slug = db.Column(db.String(80), unique=True)
    file_name = db.Column(db.String(200))
    # this is going to be used in embedding vimeo video in classroom
    vimeo_no = db.Column(db.String(50))
    premium_content = db.Column(db.Boolean)
    live = db.Column(db.Boolean)
    
    
    
    def __init__(self, lecture_no, section, title, duration, slug, file_name, vimeo_no, premium_content=True, live=True):
    
        self.lecture_no = lecture_no
        self.section = section
        self.title = title
        self.duration = duration
        self.slug = slug
        self.file_name = file_name
        self.vimeo_no = vimeo_no
        self.premium_content = premium_content
        self.live = live
    
    def __repr__(self):
        return self.title
    
        
        
        
class Premium_Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    user = db.relationship('User', backref=db.backref('premium_sale', lazy='dynamic'))
    
    registered = db.Column(db.Boolean)
    register_time_utc = db.Column(db.DateTime)
    
    def __init__(self, user, registered, register_time_utc):
        
        self.user_id = user.id
        self.registered = registered
        self.register_time_utc = register_time_utc
        
    def __repr__(self):
        return self.user_id
        
        
        
class Askquery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String(80))
    body = db.Column(db.Text)
    query_utc = db.Column(db.DateTime)
    live = db.Column(db.Boolean)
    reply_to_id = db.Column(db.Integer)
    reply = db.Column(db.Boolean)
    
    def __init__(self, user, subject, body, query_utc=None, live=False, reply_to_id=None, reply=False):
        self.user_id = user.id
        self.subject = subject
        self.body = body
        if query_utc is None :
            self.query_utc = datetime.utcnow()
        self.live = live
        self.reply_to_id = reply_to_id
        self.reply = reply
        
    def __repr__(self):
        return self.subject
    
        
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
#     post = db.relationship('Post', backref=db.backref('comment', lazy='dynamic'))
#     user = db.relationship('User', backref=db.backref('comment', lazy='dynamic'))

#     # comment is of maximum 800 characters for ease of commenting
#     body_content = db.Column(db.Text(800))
#     publish_time_utc = db.Column(db.DateTime)
#     live = db.Column(db.Boolean)
    
#     is_it_reply = db.Column(db.Boolean)
#     replied_to_comment_id = db.Column(db.Integer)
#     replied_to_post_id = db.Column(db.Integer)
#     replied_to_user_id = db.Column(db.Integer)
    
#     def __init__(self, post, user, body_content, publish_time_utc, live=True, is_it_reply=False, replied_to_comment_id=None, replied_to_post_id=None, replied_to_user_id=None):
        
#         self.post_id = post.id
#         self.user_id = user.id
#         self.body_content = body_content
#         self.publish_time_utc = publish_time_utc
#         self.live = live
#         self.is_it_reply = is_it_reply
#         self.replied_to_comment_id = replied_to_comment_id
#         self.replied_to_post_id = replied_to_post_id
#         self.replied_to_user_id = replied_to_user_id
        
#     def __repr__(self):
#         return self.id
        