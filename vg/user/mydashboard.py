from flask import session, flash, url_for, render_template, redirect
from user.models import User, Review, Invite, Meetup
from user.email_sms import send_email
from vg import db, app
import bcrypt, datetime
from website.models import Post
from user.email_sms import send_sms
from user.form import EditForm_user, EditForm_pass_user, Review_user
# initiate instamojo API
from instamojo_wrapper import Instamojo


def user_welcome_premium():
    user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()
    if user.email is not None:
        html = render_template('user/welcome-premium-mail.html', user=user)
        subject = "Congratulation! %s your payment has been successful - ValueGuyz" % user.fullname.title()
        send_email(user.email, subject, html)
        # flash(subject)
        # flash(html)
        message = "Congrats! Dost payment has been succesful. Activation may take upto 6 Hours."
        send_sms(session['mobile_ind'], message)
            
    elif user.mobile_ind :
        message = "Congrats! Dost payment has been succesful. Activation may take upto 6 Hours."
        send_sms(session['mobile_ind'], message)
            
    if session.get('mobile_invited') and session.get('invitee_mobile') :
        # for finding that unique invite and invitee_mobile linked to it
        user = User.query.filter_by(mobile_ind=session['invitee_mobile']).first()
        invite = Invite.query.filter_by(mobile_invited=session['mobile_invited'], invitee_id=user.id).first()
        if invite:
            invite.used = 1
            db.session.commit()
        else:
            message = "something wrong with invite.used for invitee %s " % user.mobile_ind
            send_sms(session['mobile_ind'], message)
        
        # write a message to invitee_mobile session get command
    
    flash('Your payment has been successful!', 'warning')
    return render_template('user/welcome-premium.html', user=user)
    
    
def user_my_dashboard_home():
    # only user with mobile registered
    user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()
    if user:
        invite_used = Invite.query.filter_by(invitee_id=user.id, used=True).count() 
        invite_sent_by_user = Invite.query.filter_by(invitee_id=user.id, used=False).order_by(Invite.invite_on_utc.desc())
        time_now = datetime.datetime.utcnow()
        invite_pending = 0
        for invite in invite_sent_by_user:
            # import pdb ; pdb.set_trace()
            if time_now - invite.invite_on_utc < datetime.timedelta(days=2):
                invite_pending = invite_pending + 1
        total_invite_spent = invite_used + invite_pending
    else:
        total_invite_spent = 0
    return render_template('user/user-dashboard-home.html', total_invite_spent=total_invite_spent)


def user_meetup():
    user = User.query.filter_by(mobile_ind=session['mobile_ind']).first_or_404()
    purpose = 'Pune meetup aug17'
    meetup_exist = Meetup.query.filter_by(user_id=user.id, purpose=purpose).first()
    # Instamojo stuff
    api = Instamojo(api_key=app.config["API_KEY"],
                    auth_token=app.config["AUTH_TOKEN"])
    # function to use further
    def pay_conference():
        response = api.payment_request_create(
            amount=200,
            buyer_name= user.fullname,
            purpose='Valueguyz Pune Con2017',
            send_email=False,
            email=user.email,
            phone=user.mobile_ind,
            redirect_url="http://www.valueguyz.com/mydashboard/meetup/confirmed",
            webhook="http://www.valueguyz.com/awnoaneon79nd"
            )
        pay_mojo = response['payment_request']['longurl']
        # this will take to external domain link
        return redirect(pay_mojo)
                    
    if meetup_exist and  meetup_exist.payment_done == True:
        flash('Your are already registered for this meetup.')
    elif meetup_exist and  meetup_exist.payment_done == False:
       return pay_conference()
    else:
        meetup = Meetup(user,
                        purpose
                        )
        db.session.add(meetup)
        db.session.flush()
        if meetup.id:
            db.session.commit()
            return pay_conference()
        else:
            db.session.rollback()
            flash('something is wrong, try after sometime.')
    return redirect(url_for('my_dashboard_home'))
    
def user_meetup_confirm():
    user = User.query.filter_by(mobile_ind=session['mobile_ind']).first_or_404()            
    flash('Congrats dost, you just reserved a seat, soon you will be notified with time n venue.')
    message = "Congrats dost, you just reserved a seat, soon you will be notified with time n venue. It would be a fun meetup. - Jasmeet Singh (Founder n Investor)"
    send_sms(user.mobile_ind, message)
    return redirect(url_for('my_dashboard_home'))
    
    

def user_my_dashboard_profile():
    #Check for unique username first & if not pass 'error' to html page
    if session.get('mobile_ind'):
        user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()
        if user is None:
            user = User.query.filter_by(email=session['mobile_ind']).first_or_404()
     # creating instance of EditForm_user form user.form which has all of Form feature too(subclass)
    form = EditForm_user()
   # --------for password purposes------
    form_pass = EditForm_pass_user()
    
    form_review = Review_user()
    # review_exist checks if user has already submittd his review and non 404 error needed
    review_exist = Review.query.filter_by(user_id=user.id).first()
    
    if form.fullname.data:
        # validate_on_submit will check if it is a POST request and if it is valid
        if form.validate_on_submit():
            fullname = user.fullname
            if form.fullname.data != fullname:
                user.fullname = form.fullname.data
                # commit all - in this case overwrite
                db.session.commit()
                flash('Your Name has been updated, Please re-login')
                return redirect(url_for('logout'))
            else:
                flash('same name entered, no need to change')
        else:
            flash('Something went wrong with Name, Retry')
    elif form_pass.current_password.data:
        # print (form_pass.errors)
        # {% if form_pass.errors %}
        # {{ form_pass.errors }}
        # {% endif %}
        # use above codes just in case error is needed to be seen on shell or html page
        # validate_on_submit will check if it is a POST request and if it is valid
        if form_pass.validate_on_submit():
            # new password should not be equal to existing password
            if form_pass.current_password.data == form_pass.new_password.data:
                flash("New password can't be same as pervious one")
            else:
                # Checks that a unhashed password matches one that has previously been
                if bcrypt.hashpw(form_pass.current_password.data, user.password) == user.password:
                    # 'salt' is a random string that is used to crypt
                    salt = bcrypt.gensalt()
                    # 'hashed_password' for the first time, with a randomly-generated salt
                    # it makes the password input by user a crypted string as 'hashed_password'
                    hashed_password_new =  bcrypt.hashpw(form_pass.new_password.data, salt)
                    user.password = hashed_password_new
                    db.session.commit()
                    flash('Your Password has been updated, Please re-login')
                    return redirect(url_for('logout'))
                else:
                    flash('Your current password is galat, Retry')
        else:
            flash('Something went wrong, Retry')
            
    elif form_review.review.data or form_review.title.data:
        if form_review.validate_on_submit() and review_exist is None:
            review = Review(
                        user,
                        form_review.rating.data,
                        form_review.title.data,
                        form_review.review.data,
                        live=False
                        )
            db.session.add(review)
            # flush will mimic the entry in database to give back 'id' just to check further
            db.session.flush()
            # now let's check if User id is there.
            if review.id:
                 # transaction or multiple insertion in databases using commit() using SQLAlchemy
                db.session.commit()
                flash('Thanks for the review dost.')
                session['review_exist'] = True
            else:
                # If any gadbad then just rollback like nothing happened & let's pass an error back
                db.session.rollback()
                flash('Error adding review')
                
        elif review_exist :
            flash('You have already given your review.')
        else:
            flash('Something went wrong, review was written properly. Retry')
    
    # for editing of review using same route
    current_time = datetime.datetime.utcnow()
    editing_karni = True
    
    if review_exist and current_time - review_exist.review_on_utc < datetime.timedelta(days=2):
        form_review = Review_user(obj=review_exist)
        if form_review.validate_on_submit():
            review_exist.rating = form_review.rating.data
            review_exist.title = form_review.title.data
            review_exist.review = form_review.review.data
            review_exist.review_on_utc = datetime.datetime.utcnow()
            review_exist.live = False
            # commit all - in this case overwrite
            db.session.commit()
            flash('Your review has been updated & will be reposted after some time.')
    else:
        editing_karni = False
    return render_template('user/user-dashboard-profile.html', form=form, user=user, form_pass=form_pass, form_review=form_review, review_exist=review_exist, editing_karni=editing_karni)
    