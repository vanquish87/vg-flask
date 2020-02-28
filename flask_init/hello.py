import os

from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    
    return url_for('show_user_profile', username='Sheena')

@app.route('/hello')
@app.route('/hello/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    return "User %s is visiting" %username


if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(host=host, port=port)
