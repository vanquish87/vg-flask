# So, in the generate_confirmation_token() function we use the URLSafeTimedSerializer 
# to generate a token using the email address obtained during user registration. 
# The actual email is encoded in the token. Then to confirm the token, within the confirm_token() function,
# we can use the loads() method, which takes the token and expiration – valid for one hour (3,600 seconds) – as arguments.
# As long as the token has not expired, then it will return an email.

# Be sure to add the SECURITY_PASSWORD_SALT to your app’s config (BaseConfig()):

from itsdangerous import URLSafeTimedSerializer

from vg import app


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
            )
            
        return email
        
    except:
        # because when we take mobile_ind and email as None in registration, it raises to a logical error so some random email
        email = "fakeemafas97234rh39f%#@D9Ksadfil@ad.cimchu"
        return email
        