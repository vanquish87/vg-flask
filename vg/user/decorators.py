# here I am creating custom decorator to check authentications of user previleges
# import a decorator named wraps 
from functools import wraps

# imports from flask library to use its methods
from flask import session, request, redirect, url_for, abort, flash

# for logged in purposes
from flask.ext.login import current_user


# decorator login_required is a subclass of 'f'
def login_required(f):
    @wraps(f)
    # args : arguments & kwargs : keyword arguments 
    # args as positional arguments
    # need to SEARCH MORE ON IT
    def decorated_function(*args, **kwargs):
        # check if session is set with 'email' (session is only set when logged in)
        if session.get('mobile_ind') is None:
            # if not in session(logged in) send to login page or 
            # load the url from address bar as 'next' variable to use it and 
            # Once logged in use 'next'to send user to that url rather than login page
            return redirect(url_for('login', next=request.url))
        # force user with only email to add mobile no.
        elif session.get('mobile_ind_exist') == False:
            flash('Dost please update your Mobile for full access')
            return redirect(url_for('update_mobile'))
        return f(*args, **kwargs)
    # return back the output value of decorated_function
    return decorated_function
    
    
# decorator login_required is a subclass of 'f'
def is_author_required(f):
    @wraps(f)
    # args : arguments & kwargs : keyword arguments 
    # args as positional arguments
    # need to SEARCH MORE ON IT
    def decorated_function(*args, **kwargs):
        # check if session is set with 'is_author' (so that only author is allowed)
        if session.get('is_author') == 0 :
            return abort(403)
        return f(*args, **kwargs)
    # return back the output value of decorated_function
    return decorated_function
    
    
def is_premium_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_premium') == 0:
            flash('You are not a valid premium member dost, activate your premium membership for full access')
            return redirect(url_for('premium_sell'))
        return f(*args, **kwargs)
    # return back the output value of decorated_function
    return decorated_function
    
def adv_course_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('adv_course') == 0:
            flash('Dost, you are not enrolled for advanced course, please buy it to activate access')
            return redirect(url_for('premium_sell'))
        return f(*args, **kwargs)
    # return back the output value of decorated_function
    return decorated_function


# # force user with only email to add mobile no.
# def add_mobile_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get('mobile_ind_exist') == False:
#             flash('Dost please update your Mobile for full access')
#             return redirect(url_for('update_mobile'))
#         return f(*args, **kwargs)
#     # return back the output value of decorated_function
#     return decorated_function
    
# # decorator to applied where it is needed if user is email verified
# def user_confirmed(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get('confirmed') == 0:
#             flash('access denied')
#             return redirect(url_for('unconfirmed'))
#         return f(*args, **kwargs)
#     return decorated_function
    