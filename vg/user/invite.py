from itsdangerous import URLSafeTimedSerializer
import string, random
from flask import session, flash, url_for, render_template, redirect
from vg import app, db
from user.models import User, Invite
import datetime
from user.form import Update_Mobile
from user.email_sms import send_sms


def generate_invitation_token(mobile_invited, invitee_mobile):
# complex random string which is already encrypted using generate_confirmation_token
# generate_confirmation_token would need mobile_invited & invitee_mobile as arguments respectively
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps([mobile_invited, invitee_mobile], salt=app.config['SECURITY_PASSWORD_SALT'])


def invitation_token(token, expiration=259200):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        mobiles = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
            )
            
        return mobiles
        
    except:
        mobiles = None
        return mobiles


def short_url_generate():
    # for creating short url
    def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
        
    short_url = id_generator()
    invite = Invite.query.filter_by(short_url=short_url).first()
    # it means short_url is already used up in some invite
    if invite:
        url_exist = True
    else:
        url_exist = False
            
    while url_exist == True:
        short_url = id_generator()
        invite = Invite.query.filter_by(short_url=short_url).first()
        if invite:
            url_exist = True
            
    return short_url
    
    

def user_invite():
    error=""
    # only user with mobile registered
    user = User.query.filter_by(mobile_ind=session['mobile_ind']).first_or_404()
    # count ka algorithm likho ab....
    invite_used = Invite.query.filter_by(invitee_id=user.id, used=True).count() 
    invite_sent_by_user = Invite.query.filter_by(invitee_id=user.id, used=False).order_by(Invite.invite_on_utc.desc())
    invites_net = Invite.query.filter_by(invitee_id=user.id).order_by(Invite.invite_on_utc.desc())
    time_now = datetime.datetime.utcnow()
    
    invite_pending = 0
    for invite in invite_sent_by_user:
        # import pdb ; pdb.set_trace()
        if time_now - invite.invite_on_utc < datetime.timedelta(days=2):
            invite_pending = invite_pending + 1
    total_invite_spent = invite_used + invite_pending
    if total_invite_spent > 1:
        allow_inviting = False
    else:
        allow_inviting = True

    # invite karne ka form and sms from here
    mobile_invited = Update_Mobile()
    if mobile_invited.validate_on_submit():
        if mobile_invited.mobile_ind.data.isdigit():
            # check if mobile_invited is already a premium user or not
            user_premium = User.query.filter_by(mobile_ind=mobile_invited.mobile_ind.data, is_premium=True).first()
            if user_premium is None:
                invite = Invite.query.filter_by(mobile_invited=mobile_invited.mobile_ind.data).first()
                if invite is not None and invite.used == True:
                    flash('%r has already used up an invitation' % mobile_invited.mobile_ind.data)
                else:
                    token = generate_invitation_token(mobile_invited.mobile_ind.data, user.mobile_ind)
                    short_url = short_url_generate()
                    invite = Invite(user,
                            mobile_invited.mobile_ind.data,
                            token,
                            short_url
                            )
                    db.session.add(invite)
                    db.session.flush()
                    if invite.id:
                        # flash(invite.invite_code)
                        db.session.commit()
                        url_invited = url_for('invitation_confirm', short_url=short_url, _external=True)
                        message_invited_1 = '(1/2) Your friend %s has invited u to join Valueguyz premium. Click here %s . Carpe Diem \m/' % (user.fullname.title(), url_invited)
                        message_invited_2 = '(2/2) To access this invitation code completely u need to create an account 1st n then click again on this code above. Use it wisely as it will expire in 3 days.'
                        invitee_message = "Dost, %s has been invited to join valueguyz family. Our fight against Sattebaaji continues..." % invite.mobile_invited
                        send_sms(invite.mobile_invited, message_invited_1)
                        send_sms(invite.mobile_invited, message_invited_2)
                        send_sms(user.mobile_ind, invitee_message)
                        flash("congrats, SMS containing invitation has been sent to %s." % invite.mobile_invited)
                        
                    else:
                        db.session.rollback()
                        flash('something is wrong, try after sometime.')
            else:
               error = "Your friend is already a Premium member."
        else:
            error = 'please enter valid 10 digit mobile no.'
            
    login_view = True
    return render_template('/user/invite.html',total_invite_spent=total_invite_spent, allow_inviting=allow_inviting, mobile_invited=mobile_invited, error=error, invites_net=invites_net, time_now=time_now, invite_used=invite_used, login_view=login_view)
    
    

def user_invitation_confirm(short_url):
    invited_token = Invite.query.filter_by(short_url=short_url, used=False).first()
    if invited_token:
        try:
            token_ = invited_token.invite_code
            mobiles = invitation_token(token_)
            # flash(mobiles[0])
            # flash(mobiles[1])
        except:
            # this in case token_ is hit expiration of 3 days
            flash('Invalid invitation')
            mobiles = None
            
        user = User.query.filter_by(mobile_ind=mobiles[0]).first()
        if user :
            if user.is_premium == 0 :
                session['mobile_invited'] = mobiles[0]
                session['invitee_mobile'] = mobiles[1]
                return redirect(url_for('premium_sell_pay', pay_for='diamond'))
            else:
                flash('You are already a premium member, dost.')
        else:
            flash('To use this invitation code you need to create an account first.')
            flash('& then click on invitation again.')
            return redirect(url_for('register'))
    else:
        flash('Invalid invitation.')
    return redirect(url_for('valueguyz_home'))