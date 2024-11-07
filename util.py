from flask import request, redirect, url_for, flash, render_template, session
import pandas as pd


def login_fn():
    if request.method == 'POST':
        df = pd.read_csv('static/user_data.csv').set_index('username')
        username = request.form['username']
        password = request.form['password']

        if username in df.index:
            if df.loc[username, 'password'] == password:
                session['username'] = username
                session['bank_name'] = df.loc[username, 'bank_name']
                session['account_number'] = df.loc[username, 'bank_account_number']
                session['debt_amount'] = df.loc[username, 'debt_amount']

                return redirect(url_for('homepage'))
        
        flash('Invalid username or password')
        return redirect(url_for('login'))
    else:
        return render_template('login.html')
    
def make_payment_fn():
    if request.method == 'POST':
        df = pd.read_csv('static/user_data.csv').set_index('username')
        payment_amount = request.form['payment_amount']
        payment_amount = float(payment_amount) if type(payment_amount) != float else payment_amount
        username = session.get('username')

        df.loc[username, 'debt_amount'] -= payment_amount
        df.to_csv('static/user_data.csv')
        session['debt_amount'] -= payment_amount
        return redirect(url_for('payment_screen'))
    else:
        return render_template('payment_screen.html',
                           username=session.get('username'),
                           debt_amount=session.get('debt_amount'),
                           debt_amount_str=f'${session.get("debt_amount"):,.2f}'
        )