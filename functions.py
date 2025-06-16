from DBAccess import *
from werkzeug.security import check_password_hash


ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           



def insert_into_visningsdata(date, behandler):
    db = dbaccess()
    try:
        cursor = db.cursor()
        sql = "INSERT INTO Visningsdata (dato, behandler) VALUES (%s, %s)"
        cursor.execute(sql, (date, behandler))
        db.commit()
    finally:
        db.close()


def signup_into_loginInfo(fornavn, efternavn, mobil, email, hashed_password):
    db = dbaccess()
    try:
        cursor = db.cursor()
        sql = """
            INSERT INTO loginInfo (fornavn, efternavn, mobil, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (fornavn, efternavn, mobil, email, hashed_password))
        db.commit()
    finally:
        db.close()

def login_into_loginInfo(email, plain_password):
    db = dbaccess()
    try:
        cursor = db.cursor()
        sql = "SELECT * FROM loginInfo WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], plain_password):
            return user
        return None
    finally:
        db.close()