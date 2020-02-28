# app is an instance of the Flask from __init.py file which is our main object & mail from flask mail
from flask import session, flash, redirect, url_for, render_template, request

# for database operation using SQLAlchemy
from vg import db, app

# for filling up the form & validating in html file, use login form for logging in
from user.form import LoginForm_user, Forgetpass_Form_user, Forgetpass_OTP, Change_Forgetpass, Newpass_Form_user

# for using(access) user in database and writing review in profile pa
from user.models import User, Review

# bcrypt password hashing and key derivation
import bcrypt, datetime, random

# for email verifications
from user.token import generate_confirmation_token, confirm_token

# for sending email
from user.email_sms import send_email, send_sms


def login_user():
    form = LoginForm_user()
    error = None
    if session.get('mobile_ind'):
        flash('You are already registered & logged in Dost. ')
        return redirect(url_for('my_dashboard_home'))
    else:
        if request.method == 'GET' and request.args.get('next'):
            # then set a 'session' with next from value stored
            session['next'] = request.args.get('next', None)
                
        if form.validate_on_submit():
            if form.email.data.isdigit():
                user = User.query.filter_by(mobile_ind=form.email.data).first()
            else:
                user = user = User.query.filter_by(email=form.email.data).first()
            if user:
                if bcrypt.hashpw(form.password.data, user.password) == user.password:
                    # import pdb ; pdb.set_trace()
                    if user.mobile_ind:
                        session['mobile_ind'] = user.mobile_ind
                    else:
                        # i am gonna use single session for verification either mobile_ind or email of user
                        session['mobile_ind'] = form.email.data
                        session['mobile_ind_exist'] = False
                        
                    session['fullname'] = user.fullname
                    session['is_author'] = user.is_author
                    session['is_premium'] = user.is_premium
                    session['adv_course'] = user.adv_course
                    
                    user.last_seen_utc = datetime.datetime.utcnow()
                    db.session.commit()
                    
                    review_exist = Review.query.filter_by(user_id=user.id).first()
                    if review_exist is None:
                        # set session that shows review button in my dashboard if user hasn't already submittd his review
                        session['review_exist'] = False
                        flash('I would request you to help out your fellow valueguyz by writing a review on how it has made you confident with investing. They are really counting on your words, it will only take 1 min.')
                        
                    # from above 'next' is set then from session cookie
                    if 'next' in session:
                        next = session.get('next')
                        session.pop('next')
                        flash(" %s, you have logged in" % session['fullname'].title())
                        return redirect(next)
                        
                    else:
                        flash(" %s, you have logged in" % session['fullname'].title())
                        return redirect(url_for('my_dashboard_home'))
                        
                else:
                    error = "Incorrect email/mobile or password"   
            else:
                error = "Incorrect email/mobile or password"
        total_user = User.query.count() 
        # to avoid ask a query button in login view pased to header_navbar macro
        login_view = True
        return render_template('user/login.html', form=form, error=error, total_user=total_user, login_view=login_view)
    
    

def user_forgot_pass():
    # creating instance of Forgetpass_Form_user from user.form for forget password feature(Form subclass)
    forget_form = Forgetpass_Form_user()
    if forget_form.validate_on_submit():
        if forget_form.email.data.isdigit():
            user = User.query.filter_by(mobile_ind=forget_form.email.data).first()
            if user:
                # send OTP sms via api here
                OTP = random.randint(100000,999999)
                session['OTP'] = OTP
                session['mobile_ind_forget'] = user.mobile_ind
                time_expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=40)
                message = 'Use OTP %d for password reset on Valueguyz n it expires at %s' %(OTP, str(time_expiration.strftime('%I:%M%p')))
                send_sms(user.mobile_ind, message)
                
                flash('An OTP has been sent to your mobile no.', 'success')
                return redirect(url_for('forgot_pass_otp'))
            else:
                flash("Sorry dost, yeh mobile not registered")
        else:
            user = User.query.filter_by(email = forget_form.email.data).first()
            if user:
                token = generate_confirmation_token(user.email)
                reset_pass_url = url_for('forget_email', token=token, _external=True)
                html = render_template('user/forget-pass-activate.html', reset_pass_url=reset_pass_url)
                subject = "%s , reset your password - ValueGuyz" % user.fullname.title()
                send_email(user.email, subject, html)
                # flash(html)
                flash('A reset password email has been sent to you, check you Inbox (or spam folder)')
                return redirect(url_for('login'))
            else:
                flash('Sorry dost, koi nai hai yeh email yha')
    # to avoid ask a query button in login view pased to header_navbar macro
    login_view = True
    return render_template('user/forgot-pass.html', forget_form=forget_form, login_view=login_view, action='enter_mobile')
    
    

def user_forgot_pass_otp():
    error=""
    form = Forgetpass_OTP()
    if session.get('mobile_ind_forget'):
        form.mobile_ind.data = session['mobile_ind_forget']
        if form.validate_on_submit() :
            if form.otp_verify.data.isdigit() == True and form.otp_verify.data == str(session['OTP']):
                session['OTP_verified'] = True
                flash('Please change your password')
                return redirect(url_for('change_forgetpass'))
            else:
                error = "invalid OTP, try again."
        # to avoid ask a query button in login view pased to header_navbar macro
        login_view = True
        return render_template('user/forgot-pass.html', form=form, login_view=login_view, error=error, action='enter_otp')
    else:
        return redirect(url_for('login'))
        
        

def user_change_forgetpass():
    form = Change_Forgetpass()
    if session.get('OTP_verified') == True:
        user = User.query.filter_by(mobile_ind=session['mobile_ind_forget']).first_or_404()
        if form.validate_on_submit():
            salt = bcrypt.gensalt()
            hashed_password_new =  bcrypt.hashpw(form.new_password.data, salt)
            user.password = hashed_password_new
            db.session.commit()
            flash("Password updated.")
            return redirect(url_for('login'))
        # to avoid ask a query button in login view pased to header_navbar macro
        login_view = True
        return render_template('user/forgot-pass.html', form=form, login_view=login_view, action='change_forgetpass')
    else:
        return redirect(url_for('login'))
        
        

def user_forget_email(token):
    email = confirm_token(token)
    try:
        # query using SQLAlchemy to check user
        user = User.query.filter_by(email=email).first_or_404()
        form = Newpass_Form_user()
        if form.validate_on_submit():
            salt = bcrypt.gensalt()
            hashed_password_new =  bcrypt.hashpw(form.password.data, salt)
            user.password = hashed_password_new
            db.session.commit()
            flash('Your Password has been updated, Please re-login')
            return redirect(url_for('my_dashboard_home'))
        return render_template('user/change-pass.html', form=form, user=user, token=token)
    except:
        flash('The forgot password link is invalid or has expired.', 'danger')
        return redirect(url_for('valueguyz_home'))