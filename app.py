from flask import Flask, render_template, request
from requests import NullHandler
from patterns import patterns
import pandas as pd

import yfinance as yf
import os

from flask import Flask, request, session, redirect, url_for, render_template
from flask.helpers import flash
from flaskext.mysql import MySQL
#from flask_sqlalchemy import SQLAlchemy
import pymysql
import re 
 
app = Flask(__name__)

app.secret_key = 'jrss'
 
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] = '10.147.20.30'
app.config['MYSQL_DATABASE_USER'] = 'jaysen'
app.config['MYSQL_DATABASE_PASSWORD'] = 'dipeshpatel'
app.config['MYSQL_DATABASE_DB'] = 'it490'
mysql.init_app(app)
 
# http://localhost:5000/login/ - this will be the login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        # Create variables for easy access
        Username = request.form['Username']
        Password = request.form['Password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM Users WHERE Username = %s AND Password = %s', (Username, Password))
        # Fetch one record and return result
        account = cursor.fetchone()
   
    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            #session['id'] = account['id']
            session['Username'] = account['Username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect Username/Password!'
    
    return render_template('index.html', msg=msg)
 
# http://localhost:5000/register - this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        # Create variables for easy access
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        Username = request.form['Username']
        Password = request.form['Password']
   
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM Users WHERE Username = %s', (Username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        #elif not FirstName or not LastName or not Username or not Password:
            #msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO Users VALUES (%s, %s, %s, %s)', (FirstName, LastName, Username, Password)) 
            conn.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/buy - this will be the add page to "buy" stocks
@app.route('/buy', methods=['GET', 'POST'])
def buy():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # Output message if something goes wrong...
    msg = ''

    if 'loggedin' in session:
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'Name' in request.form and 'Ticker' in request.form:
            # Create variables for easy access
            #Username = request.form['Username']
            Username = session['Username']
            Name = request.form['Name']
            Ticker = request.form['Ticker']
            
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO Stocks (Username, Name, Ticker) VALUES (%s, %s, %s)', (Username, Name, Ticker)) 
            conn.commit()
            msg = 'You have successfully bought the stock'
            return redirect(url_for('profile'))    
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
        return render_template('buy.html', msg=msg)
    return redirect(url_for('login'))

# http://localhost:5000/sell - this will be the remove page to "sell" stocks
@app.route('/sell', methods=['GET', 'POST'])
def sell():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # Output message if something goes wrong...
    msg = ''

    if 'loggedin' in session:
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'Name' in request.form and 'Ticker' in request.form:
            # Create variables for easy access
            #Username = request.form['Username']
            Username = session['Username']
            Name = request.form['Name']
            Ticker = request.form['Ticker']
            
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('DELETE FROM Stocks WHERE Username = %s AND Name = %s AND Ticker = %s', (Username, Name, Ticker))
            conn.commit()
            msg = 'You have successfully sold the stock'
            return redirect(url_for('profile'))    
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
        return render_template('sell.html', msg=msg)
    return redirect(url_for('login'))

@app.route('/dne')
def dne():
    return render_template('dne.html')

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        ticker = request.args.get('ticker');
        if not ticker:
            ticker='GME';
        stockData = yf.Ticker(ticker)

    

        #stockInfo = stockData.info
        #print(stockInfo)

        # User is loggedin show them the home page
        return render_template('home.html', stockData=stockData, Username=session['Username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

    #print(ticker)

       
# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('Username', None)
   # Redirect to login page
   return redirect(url_for('login'))
 
# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile(): 
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM Stocks WHERE Username = %s', [session['Username']])
        data = cursor.fetchall()
        # Show the profile page with account info
        return render_template('profile.html', data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))  
  
if __name__ == '__main__':
    app.run(debug=True)







# #
#
#SELF CODE START
#
# #


@app.route('/index2') 
def index():
    ticker = request.args.get('ticker');
    #print(ticker)

    stockData = yf.Ticker(ticker)
    stockInfo = stockData.info
    print(stockInfo)
        

    return render_template('_index.html', stockInfo=stockInfo)


'''
@app.route('/2') 
def index2():
    pattern = request.args.get('pattern', None);
    if(pattern):
        datafiles = os.listdir('datasets/daily')
        for dataset in datafiles:
            df = pd.read_csv('datasets/daily/{}'.format(dataset))
            #print (df)
            try:
                print('lol')
            except:
                pass

    return render_template('_index.html', patterns=patterns)
'''




@app.route('/alt')
def alt():
    return {
        'code' : 'success'
    }

@app.route('/snapshot')
def snapshot():
    with open('datasets/companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            print(company.split(',')[0])
            symbol = company.split(',')[0]
            df = yf.download(symbol, start="2020-01-01", end="2020-08-01")
            df.to_csv('datasets/daily/{}.csv'.format(symbol));
    return {
        'code' : 'success'
    }

