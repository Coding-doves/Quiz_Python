import os
import psycopg2


def connect_to_database():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 5432)),  # default PostgreSQL port
    )
    return conn
    

def create_database_if_not_exists():
    db_name = os.getenv("DB_NAME")

    # Connect to default 'postgres' database
    conn = psycopg2.connect(
        dbname='postgres',  # default database
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432)
    )
    conn.autocommit = True  # required to CREATE DATABASE

    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created.")
    else:
        print(f"Database '{db_name}' already exists.")

    cursor.close()
    conn.close()


def initialize_tables():
    # Connect to PostgreSQL
    db = connect_to_database()
    cursor = db.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_scores (
        id SERIAL PRIMARY KEY,
        user_id INT,
        score INT,
        total_questions INT,
        quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_attempted (
        id SERIAL PRIMARY KEY,
        user_id INT,
        quiz_score_id INT,
        question VARCHAR(255),
        user_answer VARCHAR(255),
        correct_answer VARCHAR(255),
        quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (quiz_score_id) REFERENCES quiz_scores(id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        user_id INT,
        profile_image BYTEA,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        reset_token VARCHAR(100) NOT NULL,
        token_expiry TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    db.commit()
    cursor.close()
    db.close()
