from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from functions import allowed_file

app = Flask(__name__, static_folder='public_html/static', template_folder='public_html/templates')


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
                print("I did that shit")
        
        
        
    return render_template('Upload.html')
#https://www.pullrequest.com/blog/secure-file-uploads-in-flask-filtering-and-validation-techniques/
#https://stackabuse.com/step-by-step-guide-to-file-upload-with-flask/

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/Sendmail')
def Sendmail():
    return render_template('Sendmail.html')

@app.route('/Signup')
def Signup():
    return render_template('Signup.html')

@app.route('/userSite')
def userSite():
    return render_template('userSite.html')

if __name__ == '__main__':
    app.run()