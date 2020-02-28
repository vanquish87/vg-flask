# app is an instance of the Flask from __init.py file which is our main object & mail from flask mail
from flask import render_template, redirect, url_for, session, flash, abort
from vg import db, app
# for using(access) user in database and writing review in profile pa
from user.models import User
# for filling up the form & validating in html file, use login form for logging in
from user.form import RegisterForm_user_temp, RegisterForm_user, Update_Mobile, Forgetpass_OTP
from user.email_sms import send_sms
# bcrypt password hashing and key derivation
import bcrypt, datetime, random


def user_register():
    form = RegisterForm_user_temp()
    error = None
    
    if session.get('mobile_ind'):
        flash('You are already registered & logged in Dost. ')
        return redirect(url_for('my_dashboard_home'))
    else:
        if form.validate_on_submit():
            #Check for unique username first & if not pass 'error' to html page
            user = User.query.filter_by(mobile_ind=form.mobile_ind.data).first()
            if user:
                error = 'This mobile is already registered.'
            else:
                # since validate_on_submit is not working with TelField so to use isdigit to check integer value
                if form.mobile_ind.data.isdigit():
                    session['fullname'] = form.fullname.data
                    session['mobile_ind_register'] = form.mobile_ind.data
                    # send OTP sms via api here
                    OTP = random.randint(100000,999999)
                    session['OTP'] = OTP
                    time_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=40)
                    message = 'Use OTP %d for registration on Valueguyz n it expires at %s' %(OTP, str(time_expiration.strftime('%I:%M%p')))
                    send_sms(session['mobile_ind_register'], message)
                    
                    flash('An OTP has been sent to your mobile no.', 'success')
                    return redirect(url_for('register_full'))
                else:
                    error = 'please enter valid 10 digit mobile no.'
            
        # to avoid ask a query button in login view pased to header_navbar macro
        login_view = True
            
        return render_template('user/register.html', form=form, error=error, login_view=login_view, action='temp')


def user_register_full():
    # creating instance of RegisterForm_user form user.form which has all of Form feature too(subclass)
    form = RegisterForm_user()
    # first time we run this no error but variable 'error' is defined here
    error = ""
    if session.get('mobile_ind'):
        flash('You are already registered & logged in Dost. ')
        return redirect(url_for('my_dashboard_home'))
    # elif session.get('email'):
    #     flash('You are already registered but confirm your e-mail ')
    #     return redirect(url_for('unconfirmed'))
    elif session.get('fullname') and session.get('mobile_ind_register'):
        # validate_on_submit will check if it is a POST request and if it is valid
        # recaptcha validation from google
        form.fullname.data = session['fullname']
        form.mobile_ind.data = session['mobile_ind_register']
        
        if form.validate_on_submit():
            # some deep rooted issue with session that's why str is used it shows something else in FLASH but saves different value in db
            if form.otp_verify.data.isdigit() == True and form.otp_verify.data == str(session['OTP']):
                # 'salt' is a random string that is used to crypt
                salt = bcrypt.gensalt()
                # 'hashed_password' for the first time, with a randomly-generated salt
                # it makes the password input by user a crypted string as 'hashed_password'
                hashed_password =  bcrypt.hashpw(form.password.data, salt)
                user = User(
                    # data is a method to fetch from POST method from HTTP the content
                    form.fullname.data,
                    form.mobile_ind.data,
                    hashed_password,
                    confirmed_mobile=True,
                    is_premium=False,
                    is_author=False,
                    adv_course=False
                    )
                # insert entries into the database using add(user) using SQLAlchemy
                db.session.add(user)
                # flush will mimic the entry in database to give back 'id' just to check further
                db.session.flush()
                # now let's check if User id is there.
                if user.id:
                     # transaction or multiple insertion in databases using commit() using SQLAlchemy
                    db.session.commit()
                    message = "Hi! %s,\nWelcome to valueguyz.com\nYou will be set free I promise.\nJust keep up with the updates via SMSs\n\nJasmeet Singh\nSEBI Regd." %user.fullname.title()
                    send_sms(user.mobile_ind, message)
                    flash('Registered succefully, please log-in')
                    return redirect(url_for('login'))
                    # # token generated using email for verification via sending email
                    # token = generate_confirmation_token(user.email)
                    # # This 'register' function basically acts as a controller (either directly or indirectly) for the entire process:
                    # # Handle initial registration,
                    # # Generate token and confirmation URL,
                    # # Send confirmation email,
                    # # Flash confirmation,
                    # # Log in the user, and
                    # # Redirect user.
                    # #  _external=True argument? This adds the full absolute URL that includes 
                    # # the hostname and port (http://localhost:5000, in our case.)
                    # confirm_url = url_for('confirm_email', token=token, _external=True)
                    # html = render_template('user/activate.html', confirm_url=confirm_url)
                    # subject = "%s , Please confirm your email - ValueGuyz" % user.fullname
                    # send_email(form.email.data, subject, html)
                    # # login_user(user) need to login user but how?
                    # # if everything is perfect and user is created then flash a message
                    # flash('A confirmation email has been sent via email.', 'success')
                    # flash('Please log-in')
                    # return redirect(url_for('unconfirmed'))
                else:
                    # If any gadbad then just rollback like nothing happened & let's pass an error back
                    db.session.rollback()
                    error = "Error Creating User"
            else:
                error = "invalid OTP, try again."
        # to avoid ask a query button in login view pased to header_navbar macro
        login_view = True
        return render_template('user/register.html', form=form, error=error, login_view=login_view, action='register-full')
    else:
        return redirect(url_for('register'))
        
        
def user_resend_OTP():
    if session.get('mobile_ind_register') or session.get('mobile_ind_update'):
        # send OTP sms via api here
        OTP = random.randint(100000,999999)
        session['OTP'] = OTP
        time_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=40)
        if session.get('mobile_ind_register'):
            message = 'Use OTP %d for registration on Valueguyz n it expires at %s' %(OTP, str(time_expiration.strftime('%I:%M%p')))
            send_sms(session['mobile_ind_register'], message)
            
            flash('An OTP has been sent to your mobile no.', 'success')
            return redirect(url_for('register_full'))
            
        elif session.get('mobile_ind_update'):
            message = 'Your OTP is %d n it expires at %s' %(OTP, str(time_expiration.strftime('%I:%M%p')))
            send_sms(session['mobile_ind_update'], message)
            
            flash('An OTP has been sent to your mobile no.', 'success')
            return redirect(url_for('update_mobile_verify'))
    else:
        abort(404)
        

def user_update_mobile():
    error=""
    user = User.query.filter_by(email=session['mobile_ind']).first_or_404()
    form = Update_Mobile()
    if form.validate_on_submit():
            #Check for unique mobile first & if not pass 'error' to html page
            mobile_exist = User.query.filter_by(mobile_ind=form.mobile_ind.data).first()
            if mobile_exist:
                error = 'This mobile is already registered with someone else.'
            else:
                # since validate_on_submit is not working with TelField so to use isdigit to check integer value
                if form.mobile_ind.data.isdigit():
                    session['mobile_ind_update'] = form.mobile_ind.data
                    # send OTP sms via api here
                    OTP = random.randint(100000,999999)
                    session['OTP'] = OTP
                    time_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=40)
                    message = 'Use OTP %d for updating your mobile on Valueguyz n it expires at %s' %(OTP, str(time_expiration.strftime('%I:%M%p')))
                    send_sms(session['mobile_ind_update'], message)
                    flash('An OTP has been sent to your mobile no.', 'success')
                    return redirect(url_for('update_mobile_verify'))
                else:
                    error = 'please enter valid 10 digit mobile no.'
    # to avoid ask a query button in login view pased to header_navbar macro
    login_view = True
    return render_template('user/register.html', user=user, form=form, error=error, login_view=login_view, action='update-mobile')
    
    
    
def user_update_mobile_verify():
    error=""
    user = User.query.filter_by(email=session['mobile_ind']).first_or_404()
    form = Forgetpass_OTP()
    if session.get('mobile_ind_update'):
        form.mobile_ind.data = session['mobile_ind_update']
        if form.validate_on_submit() :
            if form.otp_verify.data.isdigit() == True and form.otp_verify.data == str(session['OTP']):
                user.mobile_ind = form.mobile_ind.data
                user.confirmed_mobile = 1
                db.session.commit()
                message = 'Thanks for updating, now you will get all the updates via SMS also.'
                send_sms(session['mobile_ind_update'], message)
                return redirect(url_for('logout'))
            else:
                error = "invalid OTP, try again."
        login_view = True
        return render_template('user/register.html', form=form, login_view=login_view, error=error, action='enter_otp')
    else:
        abort(404)