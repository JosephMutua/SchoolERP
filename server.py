
from logging import exception
from django.shortcuts import render
from flask import Flask, render_template, request, url_for, session, redirect
import mysql.connector

try:
    db = mysql.connector.connect (host='localhost', user='root', passwd='',database='bravoschool')
    cursor = db.cursor()
except:
    raise exception ('Failed to open the database')
    

#Creating the WSGI web server gateway interface 

app = Flask(__name__)

app.secret_key = 'your secret key'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registersub', methods=['POST', 'GET'])
def registersub():

    mes = ''
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    email = request.form['email']
    password = request.form['password']
    cursor.execute('SELECT * FROM student_details WHERE email = %s', (email, ))
    account = cursor.fetchone()

    if account:
        mes = 'User exists. Please use a another email.'
        
        return render_template ('register.html', mes=mes)

    else:
        cursor.execute('INSERT INTO student_details (fname,lname,phone,email,password) VALUES (%s, %s, %s, %s, %s)', (fname,lname,phone,email,password, ))
        db.commit()
        
        mes = 'Account successfully created'

        return render_template ('login.html', mes=mes)

@app.route ('/loginsub', methods = ['POST', 'GET'])
def loginsub():
    mes = ''
    email = request.form['email']
    password = request.form['password']


    cursor.execute('SELECT * FROM student_details WHERE email = %s AND password = %s',(email,password, ))
    account = cursor.fetchone()
    print (account)

    if account:
        
        session['email'] = email
        

        mes = 'Login Sucessful. Welcome To BRAVO SCHOOL'
        
        return redirect(url_for('stddashboard'))

    else:
        mes = 'Wrong Email or Passowrd. Conduct the Admin'
        
        return render_template('login.html', mes = mes)


@app.route('/stddashboard')
def stddashboard():
    
    if 'email' in session:
        cursor = db.cursor()
        email = session['email']
        cursor.execute('SELECT * FROM student_details WHERE email = %s', (email, ))
        account = cursor.fetchone()
        
        id = account[0]
        fname = account[1]
        lname = account [2]
        phone = account[3]
        name = fname + " " + lname
        
        return render_template('stddashboard.html', name = name)
    else:
        return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)



