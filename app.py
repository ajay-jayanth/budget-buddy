from flask import Flask, render_template, request, session, redirect, url_for, flash
import json
import datetime

from util import login_fn, make_payment_fn, signup_fn, check_schedule_config, compute_payment_amount


name = 'Budget Buddy'
app = Flask(name) 

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

    if('goal_date' in session):
        session['payment_amount'] = compute_payment_amount(datetime.datetime.strptime(session['goal_date'], '%Y-%m-%d'), session['payment_intervals'])
        payment_date = datetime.datetime.now() + datetime.timedelta(days=session['payment_intervals'])
        session['payment_date'] = payment_date.strftime('%m-%d-%Y')
        payment_amount = session.get('payment_amount', 0)
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
    else:
        return render_template(
            'homepage.html',
            username=session.get('username'),
            bank_name=session.get('bank_name'),
            account_number=session.get('account_number'),
            debt_amount=debt_amount,  # Raw number for JavaScript
            formatted_debt_amount=formatted_debt_amount  # Formatted string for display
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

@app.route('/bank-authorization', methods=['GET'])
def bank_authorization():
    return render_template(
        'bank_authorization.html',
        bank_name=session['bank_name']
    )

@app.route('/bank-authorization/captcha-form', methods=['GET', 'POST'])
def captcha_form():
    if request.method == 'POST':
        if request.form['captcha_answer'] == 'WD54J':
            return redirect(url_for('security_question'))
        else:
            flash('Captcha answer is incorrect.')
            return render_template('captcha_form.html')
 
    return render_template('captcha_form.html')

@app.route('/security-question', methods=['GET', 'POST'])
def security_question():
    if request.method == 'GET':
        questions = [
            'What was the name of your favorite childhood pet?',
            'What year was your grandmother born?',
            'What is your favorite sport?',
            'What month was your first child born?',
            'What is your skin color?'
        ]
        return render_template(
            'security_question.html',
            questions=questions
        )
    else:
        # Redirect to login page after successful signup
        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))

@app.route('/schedule-payments-screen', methods=['GET'])
def schedule_payments_screen():
    return render_template('schedule_payments_screen.html', debt_amount=f'${session.get("debt_amount"):,.2f}')

@app.route('/schedule-payments', methods=['POST'])
def schedule_payments():
    str_goal_date = request.form['goal_date']
    goal_date = datetime.datetime.strptime(str_goal_date, '%Y-%m-%d')
    yearly_income = float(request.form['yearly_income'].removeprefix('$').replace(',', ''))
    payment_intervals = int(request.form['payment_intervals'])
    session['goal_date'] = str_goal_date
    session['payment_intervals'] = payment_intervals
    config_valid, err_str = check_schedule_config(goal_date, yearly_income, payment_intervals)
    if not config_valid:
        if err_str == 'Date':
            flash('The date is invalid.')
            return redirect(url_for('schedule_payments_screen'))
        elif err_str == 'Amount':
            flash('The amount cannot be paid before the goal date.')
            return redirect(url_for('schedule_payments_screen'))

    session['payment_amount'] = compute_payment_amount(goal_date, payment_intervals)
    payment_date = datetime.datetime.now() + datetime.timedelta(days=payment_intervals)
    session['payment_date'] = payment_date.strftime('%m-%d-%Y')

    # Add confirmation message
    # flash('Payment schedule created successfully!')
    return redirect(url_for('homepage'))

@app.route('/clear-schedule', methods=['GET'])
def clear_schedule():
    # Remove payment-related session variables
    session.pop('payment_amount', None)
    session.pop('payment_date', None)
    
    # Add a flash message to confirm schedule has been cleared
    flash('Payment schedule has been cleared.')

    return redirect(url_for('homepage'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index_function'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000, threaded=True)
