# views are controller (which has to route) in flask in MVC Pattern

# app is an instance of the Flask from __init.py file which is our main object
# for database operation using SQLAlchemy & uploading images
from vg import app, db, upload_images_post
from flask import render_template, redirect, url_for, flash, session, abort, request, send_from_directory
# for creating user in database
from user.models import User, Review
# for contact form in homepage
from user.form import ContactForm_user
# for creating a blog & others in database
from website.models import Blog, Post, Askquery
# for sending email
from user.email_sms import send_sms, send_email
import datetime
# for validating user using custom decorators
from user.decorators import login_required


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
def valueguyz_home(page=1):
    contactform = ContactForm_user()
    user = None
    if session.get('mobile_ind'):
        user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()
        if user is None:
            user = User.query.filter_by(email=session['mobile_ind']).first_or_404()
        contactform.mobile_ind.data = session['mobile_ind']
    
    if contactform.validate_on_submit():
        if user.mobile_ind :
            # after lot of search i put .data to only fetch the values without html tags oofff!!
            subject = contactform.subject.data
            body = contactform.body.data
            
            ask_query = Askquery(
                        user,
                        subject,
                        body,
                        live=True
                        )
            db.session.add(ask_query)
            db.session.flush()
            if ask_query.id:
                db.session.commit()
                # sending contact form email to jasmeet@valueguyz.com
                html = render_template('user/feedback-admin.html', user=user, subject=subject, body=body)
                subject = "%s, has sent you a Query/Feedback" % user.fullname.title()
                send_email('jasmeet@valueguyz.com', subject, html)
                # flash(html)
                # flash(ask_query.body)
                # flash(ask_query.query_utc)
                
                flash("%s ji thanks for the Query" % user.fullname.title())
                # sending acknowledgement sms to user
                message = "%s ji thanks for the Query, I would definitely look into this & revert back to you.- Jasmeet Singh (Founder & Investor)" % user.fullname.title()
                send_sms(session['mobile_ind'], message)
            else:
                db.session.rollback()
                flash('Try again, something is wrong.')
            # # sending acknowledgement email to user
            # html = render_template('user/feedback-acknowledge.html', user=user, subject=subject, body=body)
            # subject = "%s, This is an acknowledgement mail for your query/feedback to ValueGuyz" % user.fullname
            # send_email(user.email, subject, html)
            # flash('your query/feedback is succesfully submitted')
    REVIEWS_PER_PAGE = 5
    reviews = Review.query.filter_by(live=True).order_by(Review.review_on_utc.desc()).paginate(page, REVIEWS_PER_PAGE, True)
    return render_template('website/index.html', user=user, contactform=contactform, reviews=reviews)
    


@app.route('/pages/valuepicks-multibagger-vgex-performance')
def vgex_performance():
     return render_template('website/pages/valuepicks-multibagger-vgex-performance.html')
     
     
# for pagination setting a constant
POSTS_PER_PAGE = 500
@app.route('/pages/value-picks-multibagger-stocks-india')
@app.route('/pages/value-picks-multibagger-stocks-india/<int:page>')
def value_picks_multibagger_stocks_india(page=1):
    user = None
    if session.get('mobile_ind'):
        user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()
        if user is None:
            user = User.query.filter_by(email=session['mobile_ind']).first_or_404()
            
    if request.args.get('next') and session.get('is_premium'):
        flash('Access denied, this premium pick was posted outside your validity. Check your profile page for validity details.')
    elif request.args.get('next'):
        return redirect(url_for('premium_sell'))
        
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date_utc.desc()).paginate(page, POSTS_PER_PAGE, True)    
    return render_template('website/pages/value-picks-multibagger-stocks-india.html', posts=posts, user=user)
     
     
@app.route('/pages/classic/coming-soon-vg')
def coming_soon():
    return render_template('website/pages/classic/coming-soon-vg.html')
    
    
@app.route('/premium-membership')
def premium_sell(page=1):
    REVIEWS_PER_PAGE = 5
    reviews = Review.query.filter_by(live=True).order_by(Review.review_on_utc.desc()).paginate(page, REVIEWS_PER_PAGE, True)
    # login_view = True
    return render_template('website/pages/premium-sell.html', SALE_OPEN=app.config["SALE_OPEN"], reviews=reviews)
    
    
@app.route('/member/reviews')
@app.route('/member/reviews/<int:page>')
def review_member(page=1):
    REVIEWS_PER_PAGE = 4
    reviews = Review.query.filter_by(live=True).order_by(Review.review_on_utc.desc()).paginate(page, REVIEWS_PER_PAGE, True)
    return render_template('website/pages/member-reviews.html', reviews=reviews)
        

# {{ url_for('article', slug='multibagger-value-picks-dec14-ashok-alco-chem', year='2014') }}
@app.route('/posts/<year>/<slug>')
# @login_required
def article(year, slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    year = post.publish_date_utc.year
    if post.category_id != 3:
        return render_template('website/post-published.html', post=post)
    else:
        flash('Access denied')
        return redirect(url_for('valueguyz_home'))

   
# for fresher series description page
@app.route('/intro-fresher-value-pick')
def intro_fresher():
    return render_template('website/courses/intro-fresher.html')

# for advanced course description page
@app.route('/advanced-value-pick')
def advanced_value():
    return render_template('website/courses/advanced-value.html')

    
# ----------------------------------------------------------------------
# custom 404 page of not found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('website/pages/classic/notfound.html'), 404
    
    
# seo & zoho verify
@app.route('/robots.txt')
@app.route('/sitemap.xml')
@app.route('/zohoverify/verifyforzoho.html')
@app.route('/google2514d6dee714a4d8.html')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
    
    
