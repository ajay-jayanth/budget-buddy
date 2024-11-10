from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_cors import CORS
import json
import datetime

from util import login_fn, make_payment_fn, signup_fn, check_schedule_config, compute_payment_amount


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
    debt_amount = session.get("debt_amount", 0)
    formatted_debt_amount = f'${debt_amount:,.2f}'  # This is for display purposes only

    payment_amount = session.get('payment_amount', 0)

    if payment_amount == 0:
        return render_template(
            'homepage.html',
            username=session.get('username'),
            bank_name=session.get('bank_name'),
            account_number=session.get('account_number'),
            debt_amount=debt_amount,  # Raw number for JavaScript
            formatted_debt_amount=formatted_debt_amount  # Formatted string for display
        )
    else:
        return render_template(
            'homepage_SP.html',
            username=session.get('username'),
            bank_name=session.get('bank_name'),
            account_number=session.get('account_number'),
            debt_amount=debt_amount,  # Raw number for JavaScript
            formatted_debt_amount=formatted_debt_amount,  # Formatted string for display,
            payment_amount=f'${payment_amount:,.2f}',
            payment_date=session.get('payment_date')
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

@app.route('/schedule-payments-screen', methods=['GET'])
def schedule_payments_screen():
    return render_template('schedule_payments_screen.html')

@app.route('/schedule-payments', methods=['POST'])
def schedule_payments():
    goal_date = datetime.datetime.strptime(request.form['goal_date'], '%Y-%m-%d')
    yearly_income = int(request.form['yearly_income'])
    payment_intervals = int(request.form['payment_intervals'])

    config_valid, err_str = check_schedule_config(goal_date, yearly_income, payment_intervals)
    if not config_valid:
        if err_str == 'Date':
            flash('The date is invalid.')
            return redirect(url_for('schedule-payments-screen'))
        elif err_str == 'Amount':
            flash('The amount cannot be paid before the goal date.')
            return redirect(url_for('schedule-payments-screen'))
    
    session['payment_amount'] = compute_payment_amount(goal_date, payment_intervals)
    payment_date = datetime.datetime.now() + datetime.timedelta(days=payment_intervals)
    session['payment_date'] = payment_date.strftime('%m-%d-%Y')
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000, threaded=True)
