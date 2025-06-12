from flask import Flask, render_template

app = Flask(__name__, static_folder='public_html/static', template_folder='public_html/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Upload')
def Upload():
    return render_template('Upload.html')

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