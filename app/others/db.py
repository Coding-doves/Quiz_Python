import mysql.connector
from mysql.connector import errorcode

def connect_to_database():
    conn = mysql.connector.connect(
        host='localhost',
        user='ada',
        password='password',
        # database='quizapp'
    )

    return conn
