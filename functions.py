from DBAccess import connection


ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           



def insert_into_visningsdata(date, behandler):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Visningsdata (dato, behandler) VALUES (%s, %s)"
            cursor.execute(sql, (date, behandler))
        connection.commit()
    finally:
        connection.close()


def signup_into_loginInfo(connection, fornavn, efternavn, mobil, email, hashed_password):
    try:
        with connection.cursor() as cursor:
            sql = """
                    INSERT INTO loginInfo (fornavn, efternavn, mobil, email, password)
                    VALUES (%s, %s, %s, %s, %s)
                """
            cursor.execute(sql, (fornavn, efternavn, mobil, email, hashed_password))
        connection.commit()
    finally:
        connection.close()

def login_into_loginInfo(connection, email, password):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM loginInfo WHERE email = %s"
            cursor.execute(sql, (email,))
            user  = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                return user
            return None
    finally:
        connection.close()