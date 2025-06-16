from flask import Flask, render_template, request, flash, redirect, session
from werkzeug.utils import secure_filename, generate_password_hash, check_password_hash
import os
from functions import allowed_file, signup_into_loginInfo
from fileRead import extract_date_from_pdf, signup_into_loginInfo, login_into_loginInfo

app = Flask(__name__, static_folder='public_html/static', template_folder='public_html/templates')
app.secret_key = '911wasinsidejob'


UPLOAD_FOLDER = f"/home/sugrp202/journals"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/Upload', methods=['GET','POST'])
def Upload():
    if request.method == 'POST':
        Rfiles = request.files.getlist("fileInput")
        print("First step buddy")
        print(Rfiles)
        for files in Rfiles:
            print("Im here")
            if files and allowed_file(files.filename):
                filename = secure_filename(files.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                files.save(file_path)
                print("TS has been uploaded")



                date, behandler = extract_date_from_pdf(file_path)
                print("Dato fundet:", date)
                print("Behandler fundet:", behandler)

    return render_template('Upload.html')
        
        
"""
To do

Create a dbAcess file for (visningsData og loginInfo)  and import function into here and functions.py
    connection = sql.connect(
        host='localhost',
        user='sugrp202',
        password='F25-20-010-x20',
        database='visningsData',
        )

    connection = sql.connect(
        host='localhost',
        user='sugrp202',
        password='F25-20-010-x20',
        database='loginInfo',
        )


"""

        

#https://www.pullrequest.com/blog/secure-file-uploads-in-flask-filtering-and-validation-techniques/
#https://stackabuse.com/step-by-step-guide-to-file-upload-with-flask/

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/Sendmail')
def Sendmail():
    return render_template('Sendmail.html')

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        
        fornavn = request.form.get('fornavn')
        efternavn = request.form.get('efternavn')
        mobil = request.form.get('mobil')
        email = request.form.get('email')
        password = request.form.get('signup-password')
        password_repeat = request.form.get('signup-password-repeat')

        
        if password != password_repeat:
            flash("TS aint it dawg, passwords dont match stupid")
            return render_template('signup.html')

        
        hashed_password = generate_password_hash(password)

        signup_into_loginInfo()

        flash("damn you got TS on the raps big dawg")


    return render_template('signup.html')

@app.route('/userSite')
def userSite():
    return render_template('userSite.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = login_into_loginInfo(connection, email, password)
        if not user:
            flash("Login nejnej, check email eller password")
            return render_template('login.html')
        
        
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        


        flash("success yippii!")
        return redirect('/userSite')
    return render_template('login.html')

if __name__ == '__main__':
    app.run()