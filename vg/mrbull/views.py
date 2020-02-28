from vg import app
from flask import render_template, flash
from user.decorators import login_required, is_author_required


@app.route('/mrbull/dashboard')
@login_required
@is_author_required
def mrbull_dash():
     return render_template('mrbull/dashboard.html')
     
     
@app.route('/mrbull/marketwatch')
@login_required
@is_author_required
def mrbull_market():
     return render_template('mrbull/market-watch.html')
     
@app.route('/mrbull/transact')
@login_required
@is_author_required
def mrbull_transact():
     return render_template('mrbull/buy-sell.html')
     
# import requests
# @app.route('/hello')
# def hello_response():
#      response = requests.get('https://kite.trade/connect/login?api_key=p6pbl13v3ohn09m3')
#      flash(response)
#      return render_template('mrbull/buy-sell.html')
     
# http://digitalpbk.com/stock/google-finance-get-stock-quote-realtime
# http://nsetools.readthedocs.io/en/latest/index.html