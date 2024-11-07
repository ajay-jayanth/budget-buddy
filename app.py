from flask import Flask, render_template, request, session
from flask_cors import CORS
import json

from util import login_fn, make_payment_fn, signup_fn


name = 'Budget Buddy'
app = Flask(name) 
CORS(app)

app.config.update( 
    SECRET_KEY='dev'
)

@app.route('/')
def index_function(): 
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_fn()

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html',
                           username=session.get('username'),
                           bank_name=session.get('bank_name'),
                           account_number=session.get('account_number'),
                           debt_amount=f'${session.get("debt_amount"):,.2f}'
    )

@app.route('/payment-screen', methods=['GET'])
def payment_screen():
    return render_template('payment_screen.html',
                           username=session.get('username'),
                           debt_amount=session.get('debt_amount'),
                           debt_amount_str=f'${session.get("debt_amount"):,.2f}'
    )

@app.route('/make-payment', methods=['GET', 'POST'])
def make_payment():
    return make_payment_fn()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return signup_fn()

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000, threaded=True)
