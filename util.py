from flask import request, redirect, url_for, flash, render_template, session
import pandas as pd
import os
import datetime
from typing import Tuple

USER_DATA_PATH = 'static/user_data.csv'
BANK_DATA_PATH = 'static/bank_data.csv'

def signup_fn():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
        bank_name = request.form.get('bank_name')
        account_number = request.form.get('account_number')
        print(bank_name, account_number)
        # Check if user already exists in user_data.csv
        if os.path.exists(USER_DATA_PATH):
            user_df = pd.read_csv(USER_DATA_PATH)
            if username in user_df['username'].values:
                flash('Username already exists. Please choose a different one.')
                return redirect(url_for('signup'))
        
        # Retrieve debt amount from bank_data.csv
        if os.path.exists(BANK_DATA_PATH):
            bank_df = pd.read_csv(BANK_DATA_PATH)
            print("bank name",bank_df['bank_name'] == bank_name)
            print("acct_number", bank_df['account_number'] == account_number)
            debt_record = bank_df[(bank_df['bank_name'] == bank_name) & 
                                  (bank_df['account_number'] == account_number)]
            print(debt_record)
            if not debt_record.empty:
                debt_amount = debt_record.iloc[0]['debt_amount']
            else:
                flash("Bank details not found. Please verify your information.")
                return redirect(url_for('signup'))
        else:
            flash("Bank data file not found.")
            return redirect(url_for('signup'))
        
        # Append new user to user_data.csv
        new_user = {
            'username': username,
            'password': password,
            'bank_name': bank_name,
            'bank_account_number': account_number,
            'debt_amount': debt_amount
        }
        new_user_df = pd.DataFrame([new_user])

        if os.path.exists(USER_DATA_PATH):
            user_df = pd.read_csv(USER_DATA_PATH)
            user_df = pd.concat([user_df, new_user_df], ignore_index=True)
        else:
            user_df = new_user_df

        user_df.to_csv(USER_DATA_PATH, index=False)
        session.clear()
        # Redirect to login page after successful signup
        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

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
    
def check_schedule_config(goal_date: datetime.date, yearly_income: int, payment_intervals: int) -> Tuple[bool, str]:
    days_for_repayment = (goal_date - datetime.datetime.now()).days
    if days_for_repayment <= 0:
        return False, 'Date'
    if session.get('debt_amount') > yearly_income / 365 * days_for_repayment:
        return False, 'Amount'
    return True, 'Valid'

def compute_payment_amount(goal_date: datetime.date, payment_intervals: int) -> float:
    days_for_repayment = (goal_date - datetime.datetime.now()).days
    payment_per_day = session.get('debt_amount') / days_for_repayment
    return payment_per_day * payment_intervals
