import mysql.connector


def connect_to_database():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ada.070#X',
        database='quizapp'
    )
    return conn
