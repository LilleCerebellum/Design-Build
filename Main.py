from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update, and_
from datetime import datetime
import secrets
from werkzeug.utils import secure_filename
import os
import numpy as np
from scipy.signal import iirnotch, lfilter, convolve
from Filter import filteringSystem, moving_average_filter, lms_filter
from xml.etree.ElementTree import Element, SubElement, tostring


BASE_DIR = '/home/sugrp002/venv'

app = Flask(__name__)

# hvor databasen er placeret
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "files.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#database modellen som objekt
class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.Text, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    uploaded_by = db.Column(db.String(100))


app.secret_key = secrets.token_urlsafe(16)







ALLOWED_EXTENSIONS = {'atr', 'dat', 'hea'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#Lavet ud fra https://www.restack.io/p/flask-allowed-file-extensions   
#https://www.pullrequest.com/blog/secure-file-uploads-in-flask-filtering-and-validation-techniques/' 
#https://stackabuse.com/step-by-step-guide-to-file-upload-with-flask/
#https://flask.palletsprojects.com/en/stable/patterns/fileuploads/


#når filen er uploaded  læser den filen, kun linje 7 og derefter stripper alt således kun datoen er tilbage
def laes_date(filepath):
    with open(filepath, "r") as File:
        lines = File.readlines()
        newtimestamp = lines[6]
        date_str = newtimestamp.split(": ")[1].strip()
        return datetime.strptime(date_str, '%d.%m.%Y')

        
        
        



@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/Client', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        
        files = request.files.getlist("file")
        
        if not files:
            flash('Ingen fil valgt')
            return redirect(request.url)
        
        
        patient_id = request.form.get('patient_id', None)        
        if not patient_id:
           flash('Patient ID is required.')
           return redirect(request.url) 
       
       
        UPLOAD_FOLDER = f"/home/sugrp002/patients-raw/Patient_{patient_id}"
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        OUTPUT_FOLDER = f"/home/sugrp002/patients-filter/Patient_{patient_id}"

        
        
        uploaded_files = []
        timestampWith = {}
        

        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        
        
        
        
        for file in files:
            if file.filename == '':
                flash('Ingen fil valgt')
                continue
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_files.append(filename)
                uploaded_at = datetime.now()
                prefix = filename.split('.')[0]
                file.save(filepath)
                
                
                
                file_metadata = UploadedFile(
                    file_name=filename,
                    file_path=filepath,
                    file_size=os.path.getsize(filepath),
                    file_type=file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else None, 
                    #Splitter fra højre af punktum i liste og tilgår 2 ting i listen
                    uploaded_by= patient_id,
                )
                
                
                db.session.add(file_metadata)
                db.session.commit()
                
   
                
                if filename.endswith('.hea'): 
                    ny_timestamp = laes_date(filepath)
                    timestampWith[prefix] = ny_timestamp
                    
                             
        if timestampWith[prefix]:
            db.session.execute(update(UploadedFile).where(and_(UploadedFile.uploaded_by == patient_id, UploadedFile.file_name.like(f"{prefix}.%"))).values(uploaded_at=timestampWith[prefix]))
            db.session.commit()
        
        Fs = 360
        filteringSystem(files, patient_id, prefix, Fs)
        
                    
        
        
                
                
                
        if uploaded_files:
            flash('Files uploaded successfully!')
            return render_template('Acknowledgement.html', name=", ".join(uploaded_files)) #hensigt at nævne alle de uploadet filer
        else:
            flash('Filtyper ikke tilladt.')
            return redirect(request.url)

    return render_template('Client1.html')
#def client(): Lavet ud fra https://www.restack.io/p/flask-allowed-file-extensions
#https://www.pullrequest.com/blog/secure-file-uploads-in-flask-filtering-and-validation-techniques/' 
#https://stackabuse.com/step-by-step-guide-to-file-upload-with-flask/
#https://flask.palletsprojects.com/en/stable/patterns/fileuploads/



@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        return redirect(url_for('personale'))
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('MID')
        password = request.form.get('KODE')
        print(f"Username: {username}, Password: {password}")
    return redirect(url_for('personale'))
        
    
@app.route('/personale')
def personale():
    return render_template('personale.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        ID = request.form.get('patient_id')
        start_date = request.form.get('start')
        slut_date = request.form.get('slut')
        print(ID, start_date, slut_date)
        print('after')
        
        # data = UploadedFile.query.filter_by(uploaded_by=ID).all()
        # print(data)
        data = db.session.execute(db.select(UploadedFile).filter(UploadedFile.uploaded_by==ID,).filter(UploadedFile.uploaded_at >= start_date).filter(UploadedFile.uploaded_at <= slut_date)).scalars()
        for data in data:
            print(data.uploaded_by, data.file_path, data.uploaded_at)
#https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_filter_operators.htm
        
    return render_template('personale.html', results=data)    
    #return redirect(url_for('personale'))





if __name__ == "__main__":
    app.run(debug=True)