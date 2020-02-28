# flask_wtf :Simple integration of Flask and WTForms, including CSRF, file upload and Recaptcha integration
from flask_wtf import Form

# When you have to work with form data submitted by a browser view code quickly becomes very hard to read.
# There are libraries out there designed to make this process easier to manage.
# WTForms which we will handle it. It will validates the data before it gets to database.
from wtforms import StringField, validators, TextAreaField, BooleanField
# for validating category

from wtforms.ext.sqlalchemy.fields import QuerySelectField

# for validating an <input type="datetime-local">
from wtforms.fields.html5 import DateTimeField

# for getting file uploads from to feed into flask_upload
from flask_wtf.file import FileField, FileAllowed

# for Inheritance purposes
from user.form import RegisterForm_user

from website.models import Category


# creating a subclass of RegisterForm_user so that it inherits all the stuff
class SetupForm_blog(RegisterForm_user):
    blog_name = StringField('Blog Name', [
        validators.Required(),
        validators.Length(max=80)
        ])
        
# for Database operation on Category class
def categories():
    return Category.query


# Form for post so that post can be written frontend 
class PostForm(Form):
    
    # image = FileField('Image', validators=[
        # FileAllowed(['jpg', 'png'], 'Images Only!')
        # ])
    image = StringField('Image Name')
    
    title = StringField('Title', [
        validators.Required(),
        validators.Length(max=120)
        ])
        
    slug = StringField('Slug', [
        validators.Required(),
        validators.Length(max=100)
        ])
        
    description = TextAreaField('Description', [
        validators.Required(),
        validators.Length(max=800)
        ])
        
    publish_date_utc = DateTimeField('UTCtime', format='%Y-%m-%d %H:%M:%S')
    
    # QuerySelectField is going to pull out content of the selected query from table
    category = QuerySelectField('Category', query_factory=categories)
    
    new_category=StringField('New Category')
    
    
    meta_og_tags_title = TextAreaField('Meta', validators=[validators.Required()])
    

    # custom_css_files = TextAreaField('CSS', validators=[validators.Required()])
    
    image_n_video = TextAreaField('image_n_video')
    
    full_link = TextAreaField('Full_URL', validators=[validators.Required()])
    
    body_intro = TextAreaField('Body_intro', validators=[validators.Required()])
    
    table_summary = TextAreaField('Table_summary')
    
    body_details_website_box = TextAreaField('Full_content', validators=[validators.Required()])
    
    quality_value_boxes = TextAreaField('Quality_value')
    
    annual_report_table = TextAreaField('Annual_Reports')
    
    read_time = StringField('Reading Time', [
        validators.Required(),
        validators.Length(min=1, max=20)
        ])
        
    
    premium_content = BooleanField('Premium Content: (Use Tick for yes)')
    
    simple_content = BooleanField('If you dont want standard macros to be inserted in post (Use Tick for yes)')