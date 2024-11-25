from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
from datetime import datetime
from config import Config

app=Flask(__name__)
app.config.from_object(Config)
mysql=MySQL(app)
app.secret_key = 'hack'

@app.route('/')
def hello_world():
    return render_template('front.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/our_features')
def our_features():
    return render_template('our_features.html')

@app.route('/form_login',methods=['POST','GET'])
def login():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            user_id = user[0]
            session['user_id'] = user_id
            return render_template('home.html')
        else:
            return render_template('login.html', error='Invalid username or password')
     return render_template('login.html')

from flask import Flask, render_template, request, redirect, url_for, flash

@app.route('/create_account', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Username or email already exists", "error")
            return render_template('create_account.html')

        else:
            cur.execute("INSERT INTO user (email, username, password) VALUES (%s, %s, %s)", (email, username, password))
            mysql.connection.commit()
            cur.close()
            flash("Account Successfully Created. You can now login.", "success")
            return render_template('create_account.html')

    return render_template('create_account.html')


@app.route('/sender',methods=['POST','GET'])
def sender():
    if request.method == 'POST':
        
        s_source= request.form['s_source']
        s_destination = request.form['s_destination']
        s_weight = request.form['s_weight']
        # Retrieve user's ID from session
        user_id = session.get('user_id')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sender (s_id,s_source, s_destination, s_weight) VALUES (%s,%s, %s, %s)", (user_id,s_source, s_destination, s_weight))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('listprofiles_r'))
    return render_template('receiver.html')
    
@app.route('/send',methods=['POST'])
def send():
    return render_template('sender.html')

@app.route('/receive',methods=['POST'])
def receive():
    return render_template('receiver.html')

@app.route('/receiver',methods=['POST','GET'])
def receiver():
    if request.method == 'POST':
        
        r_source= request.form['r_source']
        r_destination = request.form['r_destination']
        r_weight = request.form['r_weight']
        # Retrieve user's ID from session
        user_id = session.get('user_id')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO receiver (r_id,r_source, r_destination, r_weight) VALUES (%s,%s, %s, %s)", (user_id,r_source, r_destination, r_weight))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('listprofiles_s'))
    return render_template('receiver.html')

@app.route('/list_profiles_s',methods=['POST','GET'])
def listprofiles_s():
    cur = mysql.connection.cursor()
    user_id = session.get('user_id')
    cur.execute("SELECT r_destination FROM receiver WHERE r_id = %s", (user_id,))
    destination = cur.fetchone()
    
    cur.execute("SELECT DISTINCT u.username,s.s_destination,s.s_source,s.s_weight FROM user u JOIN sender s ON u.id = s.s_id WHERE s.s_destination = %s", (destination,))
    user_data = cur.fetchall()
    cur.close()

    return render_template('r_profiles.html', user_data=user_data)
    


@app.route('/list_profiles_r',methods=['POST','GET'])
def listprofiles_r():
    cur = mysql.connection.cursor()
    user_id = session.get('user_id')
    cur.execute("SELECT s_destination FROM sender WHERE s_id = %s", (user_id,))
    destination = cur.fetchone()
    
    cur.execute("SELECT DISTINCT u.username,r.r_destination,r.r_source,r.r_weight FROM user u JOIN receiver r ON u.id = r.r_id WHERE r.r_destination = %s", (destination,))
    user_data = cur.fetchall()
    cur.close()


    return render_template('r_profiles.html', user_data=user_data)

@app.route('/send_message/<username>', methods=['GET'])
def send_message(username):
    return render_template('message.html')  



if __name__=="__main__":
    app.run(debug=True)
