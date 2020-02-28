# set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), '..')))

import unittest
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy

from flask import session
from vg import app, db
from user.models import *
from website.models import *


class UserTest(unittest.TestCase):
    def setUp(self):
        db_username = app.config['DB_USERNAME']
        db_password = app.config['DB_PASSWORD']
        db_host = app.config['DB_HOST']
        self.db_uri = "mysql+pymysql://%s:%s@%s/" % (db_username, db_password, db_host)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'sekrit!'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['RECAPTCHA_ENABLED'] = False
        app.config['MAIL_SUPPRESS_SEND'] = False
        app.config['BLOG_DATABASE_NAME'] = 'test_blog'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute('commit')
        conn.execute('CREATE DATABASE ' + app.config['BLOG_DATABASE_NAME'])
        db.create_all()
        conn.close()
        self.app = app.test_client()
        
    def tearDown(self):
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute('commit')
        conn.execute('DROP DATABASE ' + app.config['BLOG_DATABASE_NAME'])
        conn.close()
        
    def create_blog(self):
        return self.app.post('/setup', data=dict(
            blog_name='My test blog',
            fullname='My hero',
            mobile_ind='9911662211',
            otp_verify = '123456',
            password='testing123',
            confirmed_mobile=True,
            is_author=True
            ),
            follow_redirects=True)
    
    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
            ),
            follow_redirects=True)
            
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
            
            
    def test_create_blog(self):
        # it needs decrators removed if not logged in
        rv = self.create_blog()
        assert 'Blog and the user(admin) created' in str(rv.data)
        
    def test_login_logout(self):
        self.create_blog()
        
        # correct login mobile
        rv = self.login('9911662211', 'testing123')
        assert 'My Hero, you have logged in' in str(rv.data)
        
        # corrent login logout 1st
        rv = self.logout()
        assert 'See you later Dost' in str(rv.data)
        
        # less than 10 digits in mobile
        rv = self.login('991166','fsgsdfgsdfgsd')
        assert 'Incorrect email/mobile or password' in str(rv.data)
        
        # checking is digit()
        rv = self.login('991166dasd','fsgsdfgsdfgsd')
        assert 'Incorrect email/mobile or password' in str(rv.data)
        
        # checking  more than 10 digit
        rv = self.login('991166204832075034750284023804823048203580436043860348604860385038450830348603485038','fsgsdfgsdfgsd')
        assert 'Incorrect email/mobile or password' in str(rv.data)
        
        # incorrect username
        rv = self.login('wrong@user.com', 'testing123')
        assert 'Incorrect email' in str(rv.data)
        
        # incorrect password
        rv = self.login('hero@hero.io', 'testing1fadsfasd23')
        assert 'Incorrect email/mobile or password' in str(rv.data)
        
        # incorrect password (small)
        rv = self.login('hero@hero.io', 'te')
        assert 'Field must be between 6 and 60 characters long' in str(rv.data)
        
        # incorrect password (long)
        rv = self.login('hero@hero.io', 'tefadkfahsffasdifh234972597394y5394524i3y42fasdhfkasdnfoasdfuu093480r)(&()&')
        assert 'Field must be between 6 and 60 characters long' in str(rv.data)
        
        rv = self.login('fasdf','fas')
        assert 'Field must be between 6 and 60 characters long' in str(rv.data)
      
     
     
    def register(self, fullname, mobile_ind):
        return self.app.post('/register', data=dict(
            fullname=fullname,
            mobile_ind=mobile_ind
            ),
            follow_redirects=True)
        
    def register_full(self, fullname, mobile_ind, otp_verify, password):
        return self.app.post('/register-full', data=dict(
            fullname=fullname,
            mobile_ind=mobile_ind,
            otp_verify=otp_verify,
            password=password
            ),
            follow_redirects=True)
            

    def test_register(self):
        
        # less than 10 digit
        rv = self.register('jasmeet', '123456')
        assert 'please enter valid 10 digit mobile no.' in str(rv.data)
        
        # checking is.digit()
        rv = self.register('jasmeet', '123456wert')
        assert 'please enter valid 10 digit mobile no.' in str(rv.data)
        
        # checking already registered mobile
        self.create_blog()
        rv = self.register('jasmeet', '9911662211')
        # print(rv.data)
        assert 'This mobile is already registered.' in str(rv.data)
        
        # correct registration 1st
        rv = self.register('jasmeet', '1234567890')
        assert 'An OTP has been sent to your mobile no.' in str(rv.data)
        
        import flask
        app = flask.Flask(__name__)
        

        # # going further into full register
        # with app.test_request_context('/register'):
        #     level_1 = self.register('jasmeet', '1234567890')
        #     assert flask.session.args['fullname'] == 'jasmeet'
            # session is not working, go read flask testing in details & try to implement session with a simple new route first
            # rv = self.register_full(session.get('fullname'), session.get('mobile_ind_register'), session.get('OTP'), '123456')
            # print(rv.data)
            # assert 'Welcome to valueguyz.com. I personally congratulate you for joining me' in str(rv.data)
        
        # with app.test_request_context('/tough'):
        #     with app.test_client() as c:
        #         with c.session_transaction() as sess:
        #             rv = c.get('/tough')
        #             assert sess['tough'] == 'testing is confusing'
        
        # with self.app as c:
        #     with c.session_transaction() as sess:
        #         sess['logged'] = True
        #         resp = c.get('/tough')
        #     self.assertEqual('with session', resp.data)
        
        
    def testNumberIncrease(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # Modify the session in this context block.
                sess["last_num"] = "8"
            # Test the request in this context block.
            res = client.get("/increasenum")
            self.assertTrue(res is not None)
            
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # Modify the session in this context block.
                sess["tough"] = "238"
            # Test the request in this context block.
            res = client.get("/setting/tough")
            self.assertTrue(res is not None)
            

if __name__ == '__main__':
    unittest.main()