# views are controller (which has to route) in flask in MVC Pattern
# app is an instance of the Flask from __init.py file which is our main object & mail from flask mail
from vg import app
from flask import render_template, redirect, url_for, session, flash, abort, request
# for validating user using custom decorators
from user.decorators import login_required

from user.login import login_user, user_forgot_pass, user_forgot_pass_otp, user_change_forgetpass, user_forget_email

from user.register import user_register, user_register_full, user_resend_OTP, user_update_mobile, user_update_mobile_verify

from user.invite import user_invite, user_invitation_confirm

from user.mydashboard import user_welcome_premium, user_my_dashboard_profile, user_my_dashboard_home, user_meetup, user_meetup_confirm


# # sample route for testing
# @app.route('/tough')
# def tough():
#     session['tough'] = 151
#     return 'Hello tough guy!'
    
# @app.route('/setting/tough')
# def setting_tough():
#     if session.get('tough') == 151:
#         return 'It works! with %d' % session['tough']
#     else:
#         return 'session thing not working'
        

# @app.route("/increasenum", methods=["GET"])
# def increase_num():
#     if session and "last_num" in session:
#         num = session["last_num"]
#         num = str(int(num) + 1)
#         session["last_num"] = num
#         return num
#     else:
#         session["last_num"] = "0"
#         return "0"
    
    

@app.route('/login', methods=('GET', 'POST'))
def login():
    return login_user()
    
    
# this link is forget password email - registered email to be entered by user
@app.route('/forgotpassword', methods=('GET', 'POST'))
def forgot_pass():
    return user_forgot_pass()
            
            
# forgot pass otp verification route
@app.route('/forgotpassword/mobile', methods=('GET', 'POST'))
def forgot_pass_otp():
    return user_forgot_pass_otp()


@app.route('/mobile/changepass', methods=('GET', 'POST'))
def change_forgetpass():
    return user_change_forgetpass()
    
# email verification route whose link will be emailed to user to verify email   
@app.route('/confirm/pass/<token>', methods=('GET', 'POST'))
def forget_email(token):
    return user_forget_email(token)
    
@app.route('/logout')
def logout():
    if session.get('mobile_ind'):
        session.clear()
        flash('You have logged out. See you later Dost ')
        return redirect(url_for('valueguyz_home'))
    else:
        abort(404)
    

# route to temp register user with indian mobile
@app.route('/register', methods=('GET', 'POST'))
def register():
    return user_register()
    
    
# route to register new user
@app.route('/register-full', methods=('GET', 'POST'))
def register_full():
    return user_register_full()
    

@app.route('/resendOTP', methods=('GET', 'POST'))
def resend_OTP():
    return user_resend_OTP()
    
    
    
@app.route('/update-mobile', methods=('GET', 'POST'))
def update_mobile():
    if session.get('mobile_ind'):
        return user_update_mobile()
    else:
        return redirect(url_for('login', next=request.url))
    
    
    
@app.route('/update-mobile/verify', methods=('GET', 'POST'))
def update_mobile_verify():
    if session.get('mobile_ind'):
        return user_update_mobile_verify()
    else:
        return redirect(url_for('login', next=request.url))


@app.route('/invite', methods=('GET','POST'))
@login_required
def invite():
    return user_invite()


@app.route('/i/<short_url>')
def invitation_confirm(short_url):
    return user_invitation_confirm(short_url)


# this page is for user who has yet to confirm thier account, link to it is in navbar
@app.route('/mydashboard/welcome-premium')
@login_required
def welcome_premium():
    return user_welcome_premium()



# user's dashboard homepage
@app.route('/mydashboard/home')
@login_required
def my_dashboard_home():
    return user_my_dashboard_home()


    
# user's dashboard courses
@app.route('/mydashboard/courses')
def my_dashboard_course():
    return render_template('user/user-dashboard-courses.html')
    
    
# user's dashboard
@app.route('/mydashboard/profile', methods=('GET','POST'))
@login_required
def my_dashboard_profile():
    return user_my_dashboard_profile()
    
@app.route('/mydashboard/meetup')
@login_required
def meetup():
    return user_meetup()
    
@app.route('/mydashboard/meetup/confirmed')
@login_required
def meetup_confirm():
    return user_meetup_confirm()



# ----------------------------------------------------------------------------------------------------------------- 
# # user's dashboard webinars
# @app.route('/mydashboard/webinars')
# @login_required
# def my_dashboard_webinar():
#     user = User.query.filter_by(email=session['email']).first_or_404()
#     return render_template('user/user-dashboard-webinars.html', user=user)
    


# # email verification route whose link will be emailed to user to verify email   
# @app.route('/mydashboard/confirm/<token>')
# @login_required
# def confirm_email(token):
#     email = confirm_token(token)
#     try:
#         # query using SQLAlchemy to check value of confirmed_on
#         user = User.query.filter_by(email=email).first_or_404()
#         # if user has already confirmed or not
#         if user.confirmed == 1:
#             flash('Account is already confirmed.', 'success')
#         else:
#             user.confirmed = True
#             user.confirmed_on_utc = datetime.datetime.utcnow()
#             db.session.add(user)
#             db.session.commit()
#             # to send a welcome e-mail with all the notices & feautures list
#             html = render_template('user/welcome.html', user=user)
#             subject = "%s, I personally welcome you to ValueGuyz - By Jasmeet Singh" % user.fullname
#             send_email(user.email, subject, html)
#             flash('You have confirmed your account. Thanks!', 'success')
#             flash('Please log-in')
#     except:
#         flash('The confirmation link is invalid or has expired.', 'danger')
#     return redirect(url_for('logout'))
    
    
# # this page is for user who has yet to confirm thier account, link to it is in navbar
# @app.route('/mydashboard/unconfirmed')
# @login_required
# def unconfirmed():
#     # query using SQLAlchemy to check value of confirmed_on
#     user = User.query.filter_by(email=session['email']).first_or_404()
#     if user.confirmed:
#         flash('You Have already Confirmed Dost.')
#         return redirect(url_for('my_dashboard_home'))
#     flash('Please confirm your account!', 'warning')
#     return render_template('user/unconfirmed.html')


# # resending verify email just in case not done
# @app.route('/resend987')
# @login_required
# def resend_confirmation():
#     # query using SQLAlchemy to check value of confirmed_on
#     user = User.query.filter_by(email=session['email']).first_or_404()
#     token = generate_confirmation_token(user.email)
#     confirm_url = url_for('confirm_email', token=token, _external=True)
#     html = render_template('user/activate.html', confirm_url=confirm_url)
#     subject = "Please confirm your email - ValueGuyz (Resend email)"
#     send_email(user.email, subject, html)
#     flash('A new confirmation email has been sent.', 'success')
#     return redirect(url_for('unconfirmed'))
