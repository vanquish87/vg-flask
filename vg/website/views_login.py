from vg import app, db, upload_images_post
from flask import render_template, redirect, url_for, flash, session, abort, request, send_from_directory

# for validating user using custom decorators
from user.decorators import login_required, is_premium_required, adv_course_required

# for creating user in database
from user.models import User, Invite

# for creating a blog & others in database
from website.models import Post, Lecture

# initiate instamojo API
from instamojo_wrapper import Instamojo

import datetime, requests


# to view the premium pick article through this route
@app.route('/premium-pick/<year>/<slug>')
@login_required
@is_premium_required

def premium_article(year,slug):
    # check the slug from 'post' Table by query or return 404 page
    post = Post.query.filter_by(slug=slug, category_id=3).first_or_404()
    year = post.publish_date_utc.year
    user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()

    if post.publish_date_utc > user.premium_registered_on and post.publish_date_utc < user.premium_expiry_on :
        time_now = datetime.datetime.utcnow()
        if user.premium_expiry_on - time_now < datetime.timedelta(days=60) and user.premium_expiry_on - time_now > datetime.timedelta(days=0):
            flash('Your premium membership is about to expire, please renew to continue uninterrupted services.')
        elif user.premium_expiry_on - time_now < datetime.timedelta(days=0):
            flash('Your premium membership is already expired, please renew to get new premium picks.')
        return render_template('website/post-published.html', post=post)
    elif user.is_author == 1:
        return render_template('website/post-published.html', post=post)
    # else route needs further work before apr17
    else :
        flash('Access denied, this premium pick is outside you validity.')
        return abort(404)
    


@app.route('/renew-premium')
@login_required
@is_premium_required
def renew_premium():
    # session['renew_premium'] = True
    # setting for 12 month renewal
    return redirect(url_for('premium_sell_pay', pay_for='diamond'))
    

@app.route('/premium-membership/pay')
@app.route('/premium-membership/pay/<pay_for>')
@login_required
def premium_sell_pay(pay_for):
    api = Instamojo(api_key=app.config["API_KEY"],
    auth_token=app.config["AUTH_TOKEN"])
    
    user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()
    # if session.get('is_premium') == 1:
    #     session['renew_premium'] = True

    if pay_for == 'silver':
        amount = '3999'
        purpose = 'Silver (Advanced Course)'
        validity = 'Lifetime'
    elif pay_for == 'gold':
        amount = '7999'
        purpose = 'Gold (Premium 3 Months)' # use only 30 chars
        validity = '3 Months'
    elif pay_for == 'diamond':
        amount = '17999'
        purpose = 'Diamond (Premium 12 Months)'
        validity = '12 Months'
    elif pay_for == 'platinum':
        amount = '43999'
        purpose = 'Platinum (Premium 36 Months)'
        validity = '36 Months'
     
    elif pay_for == 'invitee_mobile':  
        # renew premium adjusting to invites done
        invite_used = Invite.query.filter_by(invitee_id=user.id, used=True).count() 
        purpose = 'Diamond (Premium 12 Months)'
        validity = '12 Months'
        # sort of hack to make invite work in this route
        app.config["SALE_OPEN"] = False
        if invite_used == 0:
            amount = '8999'
        elif invite_used == 1:
            amount = '4500'
        elif invite_used >= 2:
            flash('Call at 9871012220 to claim your 100% discount.')
            return redirect(url_for('invite'))
        
        
    # for 50% off sales and free user
    if app.config["SALE_OPEN"]:
        response = api.payment_request_create(
            amount=round(int(amount) / 2),
            buyer_name= user.fullname,
            purpose=purpose,
            send_email=False,
            email=user.email,
            phone=user.mobile_ind,
            redirect_url="http://www.valueguyz.com/mydashboard/welcome-premium",
            webhook="http://www.valueguyz.com/awnoaneon79nd"
            )
        pay_mojo = response['payment_request']['longurl']
        # for jinja purpose in html
        amount=round(int(amount) / 2)
    
    # for free user and normal days
    elif app.config["SALE_OPEN"] == False:
        # Create a new Payment Request
        response = api.payment_request_create(
            amount=amount,
            buyer_name= user.fullname,
            purpose=purpose,
            send_email=False,
            email=user.email,
            phone=user.mobile_ind,
            redirect_url="http://www.valueguyz.com/mydashboard/welcome-premium",
            webhook="http://www.valueguyz.com/awnoaneon79nd"
            )
        pay_mojo = response['payment_request']['longurl']
    
    # invite used here please verify with testing
    elif session.get('mobile_invited') == user.mobile_ind:
        response = api.payment_request_create(
            amount=amount,
            buyer_name= user.fullname,
            purpose='Valueguyz Premium Membership', # use only 30 chars
            send_email=False,
            email=user.email,
            phone=session['mobile_invited'],
            redirect_url="http://www.valueguyz.com/mydashboard/welcome-premium",
            webhook="http://www.valueguyz.com/awnoaneon79nd"
            )
        pay_mojo = response['payment_request']['longurl']
        
    else:
        flash('Invalid user')
        return redirect(url_for('premium_sell'))
        
    return render_template('website/pages/premium-sell-pay.html', user=user, SALE_OPEN=app.config["SALE_OPEN"], pay_mojo=pay_mojo, amount=amount, purpose=purpose, validity=validity)
        

# this is under testing abhi  
@app.route('/awnoaneon79nd', methods=['POST', 'GET'])
@login_required
def vg_webhook():
    headers = {'X-Api-Key': 'zzzz',
               'X-Auth-Token': 'zzzzzzzzzzz'}
    data = requests.get('https://www.instamojo.com/api/1.1/payment-requests/',
                 headers=headers)

    if data.get('status') == 'Credit':
        # user = User.query.filter_by(mobile_ind='9717205189').first_or_404()
        user = User.query.filter_by(email=data.get('buyer')).first_or_404()
        user.is_premium = 1
        user.premium_registered_on = datetime.datetime.utcnow()
        user.premium_expiry_on = datetime.datetime.utcnow() + datetime.timedelta(days=365)
        db.session.commit()
 

# for fresher series description page
@app.route('/mydashboard/course/content/fresher')
@login_required
def content_fresher():
    lectures = Lecture.query.filter_by(live=True, premium_content=False).order_by(Lecture.lecture_no)
    return render_template('website/courses/fresher-content.html', lectures=lectures)
    
    
# for running videos of fresher series
@app.route('/mydashboard/course/classroom/fresher/<slug>')
@login_required
def classroom(slug):
    lecture = Lecture.query.filter_by(slug=slug, premium_content=False).first_or_404()
    middle = lecture.lecture_no
    peechla = middle - 1
    agla = middle + 1
    lecture_peechla = Lecture.query.filter_by(lecture_no=peechla, premium_content=False).first()
    lecture_agla = Lecture.query.filter_by(lecture_no=agla, premium_content=False).first()
    return render_template('website/courses/classroom.html', slug=slug, lecture=lecture, lecture_peechla=lecture_peechla, lecture_agla=lecture_agla)
    

# for advanced series description page
@app.route('/mydashboard/course/content/advanced')
@login_required
@adv_course_required
def content_premium():
    lectures = Lecture.query.filter_by(live=True).order_by(Lecture.lecture_no)
    return render_template('website/courses/advanced-content.html', lectures=lectures)
    

@app.route('/mydashboard/course/classroom/advanced/<slug>')
@login_required
@adv_course_required
def classroom_premium(slug):
    lecture = Lecture.query.filter_by(slug=slug).first_or_404()
    middle = lecture.lecture_no
    peechla = middle - 1
    agla = middle + 1
    lecture_peechla = Lecture.query.filter_by(lecture_no=peechla).first()
    lecture_agla = Lecture.query.filter_by(lecture_no=agla).first()
    return render_template('website/courses/classroom-premium.html', slug=slug, lecture=lecture, lecture_peechla=lecture_peechla, lecture_agla=lecture_agla)
    
    

# # to view full article with logged in n confirmed
# @app.route('/posts/<year>/<slug>/full')
# @login_required
# @user_confirmed
# def article_full(year, slug):
#     post = Post.query.filter_by(slug=slug).first_or_404()
#     year = post.publish_date_utc.year
#      # process(rendering) this article.html page with passing post as post to fill html file
#     if post.category_id != 3:
#         return render_template('website/post-published.html', post=post)
#     else:
#         flash('Access denied')
#         return redirect(url_for('valueguyz_home'))