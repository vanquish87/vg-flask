# views are controller (which has to route) in flask in MVC Pattern

# app is an instance of the Flask from __init.py file which is our main object
from vg import app, db
from flask import render_template, redirect, url_for, flash, session, abort, request, send_from_directory

# for validating user using custom decorators
from user.decorators import login_required, is_author_required

# for creating a blog & others in database
from website.models import Blog, Post, Category, Lecture, Premium_Sale

# for filling up the form & validating in html file
from website.form import SetupForm_blog, PostForm

# for creating user in database
from user.models import User, Review, Invite, Meetup, Cron

# for contact form in homepage
from user.form import Review_user

# for sending email
from user.email_sms import send_email

import datetime

# bcrypt password hashing and key derivation
# bcrypt system hashes passwords using a version of Bruce Schneier’s Blowfish 
# block cipher with modifications designed to raise the cost of off-line password cracking.block
# The computation cost of the algorithm is parametised, so it can be increased as computers get faster
import bcrypt


# @app.route('/admin/vgex-message')
# @is_author_required
# @login_required
# def vgex_message():
#     users = User.query.order_by(User.registered_on.desc())
#     for user in users:
#         if user.mobile_ind:
#             message="%s ji, VGEX is rocked at 151%% in April. What about u? Checkout latest holdings : https://goo.gl/s9XQ4C" % user.fullname.title()
#             send_sms(user.mobile_ind, message)
#     return redirect(url_for('review_manage'))
            


@app.route('/admin/review-management/')
@app.route('/admin/review-management/<int:page>')
@is_author_required
@login_required
def review_manage(page=1):
    reviews = Review.query.order_by(Review.review_on_utc.desc())
    total_review = Review.query.filter_by(live=True).count()
    return render_template('mrgold/review-manage.html', reviews=reviews, total_review=total_review)
    
    
@app.route('/admin/edit-review/<int:review_id>', methods=('GET', 'POST'))
@is_author_required
@login_required
def review_edit(review_id):
    review = Review.query.filter_by(id=review_id).first_or_404()
    form_review = Review_user(obj=review)
    
    if form_review.validate_on_submit():
            review.rating = form_review.rating.data
            review.title = form_review.title.data
            review.review = form_review.review.data
            review.live = False
            # commit all - in this case overwrite
            db.session.commit()
            flash('updated review.')
            return redirect(url_for('review_manage'))
    return render_template('mrgold/review-edit.html', form_review=form_review, review=review)


@app.route('/admin/draft-review/<int:review_id>')
@is_author_required
@login_required
def draft_review(review_id):
    review = Review.query.filter_by(id=review_id).first_or_404()
    review.live = False
    db.session.commit()
    flash('review is now reverted to Draft (ie Not LIVE)')
    return redirect(url_for('review_manage'))
    
    
@app.route('/admin/live-review/<int:review_id>')
@is_author_required
@login_required
def live_review(review_id):
    review = Review.query.filter_by(id=review_id).first_or_404()
    review.live = True
    db.session.commit()
    flash('review is now LIVE LIVE LIVE')
    return redirect(url_for('review_manage'))
    

@app.route('/admin/draft-post/<int:post_id>')
@is_author_required
@login_required
def draft_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash('Post is now reverted to Draft (ie Not LIVE)')
    return redirect('/admin')
    
    
@app.route('/admin/live-post/<int:post_id>')
@is_author_required
@login_required
def live_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = True
    db.session.commit()
    flash('Post is now reverted to Live Mode')
    return redirect('/admin')
    

# <!--faadu amazing logic \m/--> for Admin user managerment looping purpose
# {% for premium_sale in premium_sales %}
# {% if premium_sale.user.id == user.id %}
# <td>Yes</td>
# {% endif %}
# {% endfor %}
@app.route('/admin/user-management/')
@app.route('/admin/user-management/<int:page>')
@is_author_required
@login_required
def user_management(page=1):
    USER_PER_PAGE = 100
    users = User.query.order_by(User.registered_on.desc())
    total_user = User.query.count()
    # total_registered = Premium_Sale.query.filter_by(registered=True).count()
    time_now = datetime.datetime.utcnow()
    # premium_sales = Premium_Sale.query.filter_by(registered=True)
    total_premium = User.query.filter_by(is_premium=True).count()
    total_mobile = User.query.filter_by(confirmed_mobile=True).count()
    total_mob_prem = User.query.filter_by(confirmed_mobile=True, is_premium=True).count()

    return render_template('mrgold/user-management.html', users=users, total_user=total_user, time_now=time_now, total_premium=total_premium, total_mobile=total_mobile, total_mob_prem=total_mob_prem)  
    

@app.route('/admin/premiun-management/')
@app.route('/admin/premium-management/<int:page>')
@is_author_required
@login_required
def premium_management(page=1):
    premium_users = User.query.order_by(User.premium_expiry_on)
    time_now = datetime.datetime.utcnow()
    total_premium = User.query.filter_by(is_premium=True).count()
    total_mob_prem = User.query.filter_by(confirmed_mobile=True, is_premium=True).count()
    
    return render_template('mrgold/premium-manage.html', premium_users=premium_users, time_now=time_now, total_premium=total_premium, total_mob_prem=total_mob_prem)


@app.route('/admin/invite-management/')
@app.route('/admin/invite-management/<int:page>')
@is_author_required
@login_required
def invite_management(page=1):
    invites_net = Invite.query.order_by(Invite.invite_on_utc.desc())
    time_now = datetime.datetime.utcnow()
    
    return render_template('mrgold/invite-manage.html', invites_net=invites_net, time_now=time_now)
    

@app.route('/admin/meetup-management/')
@app.route('/admin/meetup-management/<int:page>')
@is_author_required
@login_required
def meetup_management(page=1):
    meetups_net = Meetup.query.order_by(Meetup.registered_utc.desc())
    return render_template('mrgold/meetup-manage.html', meetups_net=meetups_net)


@app.route('/admin/cron-management/')
@app.route('/admin/cron-management/<int:page>')
@is_author_required
@login_required
def cron_management(page=1):
    cron_net = Cron.query.order_by(Cron.sent_utc.desc())
    india_time = datetime.timedelta(hours=5, minutes=30)
    return render_template('mrgold/cron-manage.html', cron_net=cron_net, india_time=india_time)



@app.route('/admin/sample-post')
@is_author_required
@login_required
def sample_post():
    return render_template('website/posts/sample1.html')
    

# for pagination setting a constant
POSTS_PER_PAGE = 500

@app.route('/admin/index')
# for paginated pages
@app.route('/admin/index/<int:page>')
@is_author_required
@login_required
def index(page=1):
    # query.count() is a method in SQLAlchemy to check the numbers of entries
    blog = Blog.query.first()
    if not blog:
        return redirect(url_for('setup'))
    # query posts in db with flag 'live'6 with order of publish_date_utc 
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date_utc.desc()).paginate(page, POSTS_PER_PAGE, True)

    return render_template('website/index_.html', blog=blog, posts=posts)



@app.route('/admin')
# for paginated pages
@app.route('/admin/<int:page>')
# custom decorator for authentication - check user/decorators.py
@is_author_required
@login_required

def admin(page=1):
    user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()
    if session.get('is_author') == 1:
        # query posts in db with order of publish_date_utc & specific category
        posts = Post.query.order_by(Post.publish_date_utc.desc()).paginate(page, POSTS_PER_PAGE, True)
        return render_template('mrgold/post-manage.html', posts=posts, user=user)
    else:
        abort(403)
        


@app.route('/admin/post', methods=('GET', 'POST'))
# custom decorator for authentication - check user/decorators.py
@is_author_required
@login_required

def post():
     # creating instance of PostForm from user/form.py which has all of Form feature too(subclass)
    form = PostForm()
    # validate_on_submit will check if it is a POST request and if it is valid
    if form.validate_on_submit():
        #  for catching image from the form on HTML page
        # image = request.files.get('image')
        # imagename = None
        # try something & if it doesn't work flash message
        # try:
            # imagename = upload_images_post.save(image)
        # except:
            # flash("Image was not uploaded")
        image = form.image.data
        # first let's check if there is a new category or using existing category
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            # insert entries into the database using add(new_category) using SQLAlchemy
            db.session.add(new_category)
            # flush will mimic the entry in database to give back 'id' just to check further
            db.session.flush()
            # load new_category into category so that it can now be stored
            category = new_category
            
        if form.category.data:
            # is this step really needed ? or directly load in the category?
            # get_pk is get primary key method
            category_id = form.category.get_pk(form.category.data)
            category = Category.query.filter_by(id=category_id).first()

        # assuming only 1 blog exist in database
        blog = Blog.query.first()
        # check the user who posted the form here
        user = User.query.filter_by(mobile_ind=session['mobile_ind']).first()
        # load title from form
        title = form.title.data
        slug = form.slug.data
        description = form.description.data
        # do something about it
        publish_date_utc = form.publish_date_utc.data
        meta_og_tags_title = form.meta_og_tags_title.data
        image_n_video = form.image_n_video.data
        full_link = form.full_link.data
        body_intro = form.body_intro.data
        table_summary = form.table_summary.data
        body_details_website_box = form.body_details_website_box.data
        quality_value_boxes = form.quality_value_boxes.data
        annual_report_table = form.annual_report_table.data
        read_time = form.read_time.data
        premium_content = form.premium_content.data
        simple_content = form.simple_content.data
    
        # now instantiate Post for db operation
        # 'imagename' is the saved image
        post = Post(blog, user, title, category, slug, description, meta_og_tags_title, image_n_video, full_link, body_intro, table_summary, body_details_website_box, read_time, quality_value_boxes, annual_report_table, premium_content, image, simple_content)
        
        # Repeat : insert entries into the database using add(post) using SQLAlchemy
        db.session.add(post)
        db.session.commit()
        
        year = post.publish_date_utc.year
        if post.live == False:
            flash("Post is now in Draft Mode")
        else:
            flash("Live Live Live...")
            
        if post.premium_content == 1:
            return redirect(url_for('premium_article', slug=slug, year=year))
        else:
            return redirect(url_for('article', slug=slug, year=year))
    
    # process(rendering) this post.html page with passing form as form to fill html file
    return render_template('website/post.html', form=form, action="new")
 
 
 
@app.route('/admin/edit-post/<int:post_id>', methods=('GET', 'POST'))
@is_author_required
@login_required

def edit_post(post_id):
    imagename = None
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post)
    flash("Now you are in Editing Mode")
    
    if form.validate_on_submit():
        # original_image = post.image
        # image = request.files.get('image')
        # try:
            # imagename = upload_images_post.save(image)
        # except:
            # flash("The image was not uploaded")
        # if imagename:
            # post.image = imagename
        # else:
            # post.image = original_image 
          
        imagename = post.image
        if imagename == form.image.data:
            pass
        else:
            post.image = form.image.data
            
        publish_date_utc = post.publish_date_utc
        if publish_date_utc == form.publish_date_utc.data:
            pass
        else:
            post.publish_date_utc = form.publish_date_utc.data
            
        title = post.title
        if title == form.title.data:
            # title = Post.query.filter_by(title=post.title).first()
            pass
        else:
            post.title = form.title.data
        # first let's check if there is a new category or using existing category
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            # insert entries into the database using add(new_category) using SQLAlchemy
            db.session.add(new_category)
            # flush will mimic the entry in database to give back 'id' just to check further
            db.session.flush()
            # load new_category into category so that it can now be stored
            category = new_category
            
        if form.category.data:
            # is this step really needed ? or directly load in the category?
            # get_pk is get primary key method
            category_id = form.category.get_pk(form.category.data)
            # category = Category.query.filter_by(id=category_id).first()
            post.category_id = category_id
            # reverting back to draft so that category sensitive changes to be done first before LIVE
            post.live = False
            flash("Post is now in Draft Mode since category is changed")

        slug = post.slug
        if slug == form.slug.data:
            slug = Post.query.filter_by(slug=post.slug).first()
            pass
        
        else:
            post.slug = form.slug.data
            
        description = post.description
        if description == form.description.data:
            pass
        else:
            post.description = form.description.data
            
        meta_og_tags_title = post.meta_og_tags_title
        if meta_og_tags_title == form.meta_og_tags_title.data:
            pass
        else:
            post.meta_og_tags_title = form.meta_og_tags_title.data
            
        
        image_n_video = post.image_n_video
        if image_n_video != form.image_n_video.data:
            post.image_n_video = form.image_n_video.data
            
        full_link = post.full_link
        if full_link == form.full_link.data:
            pass
        else:
            post.full_link = form.full_link.data
            
        body_intro = post.body_intro
        if body_intro == form.body_intro.data:
            pass
        else:
            post.body_intro = form.body_intro.data
        
        table_summary = post.table_summary
        if table_summary != form.table_summary.data:
            post.table_summary = form.table_summary.data
        
        body_details_website_box = post.body_details_website_box
        if body_details_website_box == form.body_details_website_box.data:
            pass
        else:
            post.body_details_website_box = form.body_details_website_box.data
            
        quality_value_boxes = post.quality_value_boxes
        if quality_value_boxes == form.quality_value_boxes.data:
            pass
        else:
            post.quality_value_boxes = form.quality_value_boxes.data
            
        annual_report_table = post.annual_report_table
        if annual_report_table == form.annual_report_table.data:
            pass
        else:
            post.annual_report_table = form.annual_report_table.data
            
        read_time = post.read_time
        if read_time != form.read_time.data:
            post.read_time = form.read_time.data
        
        premium_content = post.premium_content
        if premium_content != form.premium_content.data:
            post.premium_content = form.premium_content.data
        
        simple_content = post.simple_content
        if simple_content != form.simple_content.data:
            post.simple_content = form.simple_content.data
        
        # commit all - in this case overwrite
        db.session.commit()
        
        # for passing in redirect url
        slug = post.slug
        year = post.publish_date_utc.year
        
        flash("read time is %d" %post.read_time)
        flash("Premium Content: %s" %post.premium_content)
        flash("post publish time is: %s" %post.publish_date_utc)
        flash("image is : %s" %post.image)
        flash("Simple Content: %s" %post.simple_content)
        flash("Post is live : %s" %post.live)
        flash("Post Category is : %s" %post.category.name)
        
        if post.premium_content == 1:
            return redirect(url_for('premium_article', slug=slug, year=year))
        else:
            return redirect(url_for('article', slug=slug, year=year))
        
    else:
        flash("something is wrong")
    
    return render_template('website/post.html', form=form, post=post, action="edit")
    
 
@app.route('/admin/testing')
@is_author_required
@login_required

def test():
    return render_template('mrgold/testing.html')  

@app.route('/admin/setup', methods=('GET', 'POST'))
@is_author_required
@login_required

def setup():
    # creating instance of RegisterForm_user from user.form which has all of Form feature too(subclass)
    form = SetupForm_blog()
    # first time we run this no error but variable 'error' is defined here
    error = ""
    # validate_on_submit will check if it is a POST request and if it is valid
    if form.validate_on_submit():
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
            is_author=False
            )
        # insert entries into the database using add(user) using SQLAlchemy
        db.session.add(user)
        # flush will mimic the entry in database to give back 'id' just to check further
        db.session.flush()
        # now let's check if User id is there.
        if user.id:
            blog = Blog(
                form.blog_name.data,
                user.id
                )
            # Repeat : insert entries into the database using add(blog) using SQLAlchemy
            db.session.add(blog)
            # flush will mimic the entry in database to give back 'id' just to check further
            db.session.flush()
        else:
            # If any gadbad then just rollback like nothing happened & let's pass an error back
            db.session.rollback()
            error = "Error Creating User"
        # now check if both user.id and blog.id are created
        if user.id and blog.id:
            # transaction or multiple insertion in databases using commit() using SQLAlchemy
            db.session.commit()
            # if everything is perfect and user & blog created then flash a message
            flash("Blog and the user(admin) created")
            return redirect(url_for('valueguyz_home'))
        else:
            # If any gadbad then just rollback like nothing happened & let's pass an error back
            db.session.rollback()
            error = "Error Creating Blog"
    
    # process(rendering) this setup.html page with passing form as form & error as error to fill html file
    return render_template('website/setup.html', form=form, error=error)
    
    
 
# # this route is inactive now
# @app.route('/premium-membership/register')
# @is_author_required
# @login_required
# def premium_sell_register():
#     if session.get('email') or session.get('mobile_ind'):
#         user = User.query.filter_by(email=session['email']).first_or_404()
#         if user.is_premium == 1:
#             flash('You are already a premium member dost.')
#         else:
#             premium_sale = Premium_Sale.query.filter_by(user_id=user.id).first()
#             if premium_sale:
#                 flash("You are already registered for this sale.")
#             else:
#                 user_id = user
#                 registered = True
#                 register_time_utc = datetime.datetime.utcnow()
#                 premium_sale = Premium_Sale(user_id, registered, register_time_utc)
#                 db.session.add(premium_sale)
#                 db.session.commit()
#                 flash('Congrats, now your are eligible to participate in coming membership sale.')
#                 # to send a welcome e-mail with all the notices & feautures list
#                 batch_date = "8:00PM on 20<sup>th</sup>, May16."
#                 html = render_template('user/sale-how.html', user=user, batch_date=batch_date)
#                 subject = "%s, Congo, you are now registered for premium membership sale" % user.fullname
#                 send_email(user.email, subject, html)
#                 # flash('registrations are closed.')
#     # elif session.get('email'):
#     #     flash("Please first confirm your email id.")
#     else:
#         flash('Please login first.')
#     return redirect(url_for('premium_sell'))
    
    
# ----------------------------------------- Testing route for IP tracing
# postal_hero = False

# # Default route, print user's IP
# @app.route('/ip')
# def ipadress():
#     global postal_hero
#     if postal_hero is False and request.headers.getlist("X-Forwarded-For"):
#         ip_grouping = request.headers.getlist("X-Forwarded-For")[0]
#         ip_in_list = ip_grouping.split(', ')
#         postal_hero = ip_in_list[0]
#         return redirect(url_for('value_picks_multibagger_stocks_india'))
        
#     if postal_hero :
#         return render_template('mrgold/11.html', postal_hero=postal_hero)
# --------
#     # if request.headers.getlist("X-Forwarded-For"):
#     #   ip_grouping = request.headers.getlist("X-Forwarded-For")[0]
#     #   ip_in_list = ip_grouping.split(', ')
#     #   ip = ip_in_list[0]
    # else:
    #   ip = request.remote_addr
    # return render_template('mrgold/11.html', user_ip=ip)
        

    