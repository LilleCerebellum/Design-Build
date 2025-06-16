import mysql.connector

class dbaccess:
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='sugrp202', 
            password='F25-20-010-x20',
            host='localhost',
            database='sugrp202'
        )

    def cursor(self):
        return self.conn.cursor(buffered=True, dictionary=True)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
