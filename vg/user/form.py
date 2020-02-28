# flask_wtf :Simple integration of Flask and WTForms, including CSRF, file upload and Recaptcha integration
from flask_wtf import Form, RecaptchaField


# When you have to work with form data submitted by a browser view code quickly becomes very hard to read.
# There are libraries out there designed to make this process easier to manage.
# WTForms which we will handle it. It will validates the data before it gets to database.
from wtforms import validators, StringField, PasswordField, TextAreaField

# for validating a email id
from wtforms.fields.html5 import EmailField, IntegerRangeField, TelField

class RegisterForm_user_temp(Form):
    fullname = StringField('Full Name', [
        validators.Required(),
        validators.Length(min=4, max=80)],
        description="Enter fullname"
        )
        
    mobile_ind = TelField('Mobile', [
        validators.required(),
        validators.Length(min=10, message="please enter valid 10 digit mobile no.")]
        )
        

# creating a subclass of Form so that it inherits all the stuff
class RegisterForm_user(Form):
    fullname = StringField('Full Name', [
        validators.Required(),
        validators.Length(min=4, max=80)],
        description="Enter fullname"
        )
        
    mobile_ind = TelField('Mobile', [
        validators.required(),
        validators.Length(min=10)]
        )
        
    otp_verify = TelField('OTP', [
        validators.required(),
        validators.Length(min=6, message="invalid OTP, try again.")]
        )
    
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=6, max=60)
        ])
        
    

# LoginForm_user is for getting values for login into the app as user ie, email & password
class LoginForm_user(Form):
    email = StringField('Email / Mobile', [validators.Required()],
        description="Enter registered Email / Mobile"
        )
        
    password = PasswordField('Password', [
        validators.Required(),
        validators.Length(min=6, max=60)
        ])
        
    # recaptcha = RecaptchaField()
    
    
    
# creating a subclass of Form so that it inherits all the stuff
class EditForm_user(Form):
    fullname = StringField('Full Name', [
        validators.Length(min=4, max=80)],
        description="Enter fullname"
        )
    
    
class EditForm_pass_user(Form):
    
    current_password = PasswordField('Current Password', [
        validators.Required(),
        validators.Length(min=6, max=60)
        ])
    
    new_password = PasswordField('New Password', [
        validators.EqualTo('confirm_password', message='Passwords must match'),
        validators.Length(min=6, max=60)
        ])
        
    confirm_password = PasswordField('Repeat Password')
    
    
    
# for capturing email in case of forget password
class Forgetpass_Form_user(Form):
    
    email = StringField('Email / Mobile', [validators.Required()],
        description="Enter registered Email / Mobile"
        )
        
class Forgetpass_OTP(Form):
    
    mobile_ind = TelField('Mobile', [
        validators.required(),
        validators.Length(min=10)]
        )
    
    otp_verify = TelField('OTP', [
        validators.required(),
        validators.Length(min=6, message="invalid OTP, try again.")]
        )
        
class Change_Forgetpass(Form):
    
    new_password = PasswordField('New Password', [
        validators.EqualTo('confirm_password', message='Passwords must match'),
        validators.Length(min=6, max=60)
        ])
        
    confirm_password = PasswordField('Repeat Password')
        
        
# creating a subclass of Form so that it inherits all the stuff
class Newpass_Form_user(Form):
    fullname = StringField('Full Name', [
        validators.Length(max=80)],
        description="Enter fullname"
        )
        
    email = EmailField('Email', [
        validators.Length(max=80)],
        description="Enter Email"
        )
    
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm_password', message='Passwords must match'),
        validators.Length(min=6, max=60)
        ])
        
    confirm_password = PasswordField('Repeat Password')
    
   
    
# contact form with login required
class ContactForm_user(Form):
    fullname = StringField('Full Name', [
        validators.Length(max=80)],
        description="Enter fullname"
        )
        
    mobile_ind = TelField('Mobile', [
        validators.Length(min=10)]
        )
        
    # email = StringField('Email / Mobile', [
    #     validators.Length(max=80)],
    #     description="Enter Email/Mobile"
    #     )
        
    subject = StringField('Subject', [
        validators.Required(),
        validators.Length(min=3, max=80)
        ])
        
    body = TextAreaField('Message', [
        validators.Required(),
        validators.Length(min=6, max=800)
        ])
        
        
        
# review from for premium user
class Review_user(Form):
    rating = IntegerRangeField('Rating')
    
    title = StringField('Title', [
        validators.Required(),
        validators.Length(max=100, message='Use 100 words (Max.)')
        ])
        
    review = TextAreaField('Review', [
        validators.Required(),
        validators.Length(min=20, max=1000)
        ])
        
        

# for capturing email of email_invited
class Email_invited(Form):
    email = EmailField('Email', [
        validators.Required(),
        validators.Length(max=80)
        ],
        description="Your friend's Email"
        )
 
 
class Update_Mobile(Form):
    mobile_ind = TelField('Mobile', [
        validators.required(),
        validators.Length(min=10, message="please enter valid 10 digit mobile no.")]
        )