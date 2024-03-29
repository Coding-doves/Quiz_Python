from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import bcrypt
import mysql.connector
from quiz import Quiz
import random
import os

app = Flask(__name__)

# Generate a random secret key
secret_key = os.urandom(24)
print(secret_key)
# Set the secret key for session
app.secret_key = secret_key

# Connect to mysql db
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Ada.070#X',
    database='quizapp'
)
cursor =db.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  first_name VARCHAR(255),
                  last_name VARCHAR(255),
                  username VARCHAR(255) UNIQUE,
                  password VARCHAR(255)
                  )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_scores (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  user_id INT,
                  score INT,
                  total_questions INT,
                  quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id)
                  )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_attempted (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  user_id INT,
                  quiz_score_id INT, 
                  question VARCHAR(255),
                  user_answer VARCHAR(255),
                  correct_answer VARCHAR(255),
                  quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id),
                  FOREIGN KEY (quiz_score_id) REFERENCES quiz_scores(id)
                  )''')
db.commit()


@app.route("/", methods=['GET', 'POST'])
def login():
    """Authenticating user """
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        passwd = data.get('password')

        query = "SELECT id, password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        value = cursor.fetchone()

        if value:
            user_id, hashed_password = value
            if bcrypt.checkpw(passwd.encode('utf-8'), hashed_password.encode('utf-8')):
                # Set session variable for logged in user
                session['user_id'] = user_id
                session['username'] = username
                session['logged_in'] = True
                print('Valid user\n')
                return redirect(url_for('quiz'))
            else:
                print('wrong password\n')
                return render_template('login.html', message="Wrong password")
        else:
            print("User don't exist\n")
            return render_template('login.html', message="User not found")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    ''' creating a new user '''
    if request.method == 'POST':
        data = request.form
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        password = data.get('password')

        # Ensure password is at least 6 character
        if len(password) < 6:
            return render_template('signup.html', error='Password must be at least six characters long')

        # encrypt the password
        hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            # insert new users into table
            query = 'INSERT INTO users (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)'
            cursor.execute(query, (firstname, lastname, username, hashed_passwd))
            db.commit()

            return redirect(url_for('login'))
        except Exception as e:
            # if registration fails return response
            return render_template('signup.html', error=str(e))
    
    return render_template('signup.html')


@app.route('/quiz')
def quiz():
    ''' output to browser '''
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    # api endpoint
    api_url = "https://the-trivia-api.com/v2/questions"

    # create Quiz instance
    quiz = Quiz(api_url)
    random.shuffle(quiz.questions)
    # print("Quiz Questions:", quiz.questions)
    return render_template('quiz.html', questions=quiz.questions)


@app.route('/submit', methods=['POST'])
def submit():
    ''' handle form returned data '''
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    score = 0
    total_questions = int(request.form.get('total_questions'))
    question_data = []

    for key, value in request.form.items():
        if key.startswith('opt'):
            que_index = key[3:] # Extract index of the question
            question_key = 'question' + que_index
            correct_answer_key = 'correct' + que_index

            question = request.form.get(question_key)
            correct_ans = request.form.get(correct_answer_key)

            # gather questions data for table display
            question_data.append({
                'question': question,
                'user_answer': value,
                'correct_answer': correct_ans
            })
            
            # increase score by 1 for correct answer
            if value == correct_ans:
                score += 1

    # Insert quiz score into quiz_score table
    cursor.execute('''INSERT INTO quiz_scores (user_id, score, total_questions)
                      VALUES (%s, %s, %s)''', (user_id, score, total_questions))

    db.commit()

    # Retrieve quiz_score_id
    quiz_score_id = None
    if cursor.lastrowid is not None:
        quiz_score_id = cursor.lastrowid

    # Insert attempted quiz data into quiz_attempted table
    if quiz_score_id is not None:
        for attempt in question_data:
            cursor.execute('''INSERT INTO quiz_attempted (user_id, question, user_answer, correct_answer, quiz_score_id)
                              VALUES (%s, %s, %s, %s, %s)''', (user_id, attempt['question'], attempt['user_answer'], attempt['correct_answer'], quiz_score_id))

    db.commit()

    return render_template('result.html',
        score=score,
        total_questions=total_questions,
        question_data=question_data)


@app.route('/dashboard')
def dashboard():
    ''' display users personal data '''
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    # print(user_id)

    # Retrieve username
    cursor.execute('''SELECT username FROM users WHERE id = %s''', (user_id,))
    username = cursor.fetchone()[0]
    print(username)

    # Retrieve quiz data for the user
    cursor.execute('''SELECT id, score, total_questions, quiz_date FROM quiz_scores WHERE user_id = %s ORDER BY quiz_date DESC''', (user_id,))
    quiz_metadata = cursor.fetchall()

    # Convert quiz_metadata tuples to dictionaries for easier access
    quiz_metadata = [{'quiz_date': row[3], 'score': row[1], 'total_questions': row[2], 'id': row[0]} for row in quiz_metadata]

    # for dat in quiz_metadata:
        # print(dat['score'])
        # print(dat['quiz_date'])
        # print(dat['total_questions'])
    
    api_endpoint = request.url_root + url_for('attempted_question_api')
    
    return render_template(
        'dashboard.html',
        username=username,
        quiz_metadata=quiz_metadata,
        api_endpoint=api_endpoint)


@app.route('/view_quiz/<int:quiz_score_id>')
def view_quiz(quiz_score_id):
    """display specific quiz data"""
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    # query db for specific quiz
    cursor.execute('''SELECT question, user_answer, correct_answer FROM quiz_attempted WHERE quiz_score_id = %s AND user_id = %s''',
                   (quiz_score_id, user_id))
    quizzes = cursor.fetchall()

    # Convert quiz_metadata tuples to dictionaries for easier access
    quiz_metadata = [{'question': row[0], 'user_answer': row[1], 'correct_answer': row[2]} for row in quizzes]

    return render_template('view_quiz.html', quizzes=quiz_metadata)


@app.route('/questions')
def attempted_question_api():
    """Retrieve latest 20 attempted_quiz data in JSON"""
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    # Query the database for latest 20 quiz data
    cursor.execute('''SELECT qa.id, qa.question, qa.user_answer, qa.correct_answer 
                      FROM quiz_attempted qa
                      JOIN users u ON qa.user_id = u.id
                      WHERE u.id = %s
                      ORDER BY qa.quiz_date DESC 
                      LIMIT 20''', (user_id,))
    quizzes = cursor.fetchall()

    json_quiz = []
    for row in quizzes:
        # Ensure all elements of the row are defined
            quiz_data = {
                "id": row[0],
                "text": row[1],
                "answer": [
                    {"text": row[2], "correct": row[3] == row[2]},
                    {"text": row[3], "correct": True}
                ]
            }
            json_quiz.append(quiz_data)

    # Return the data as JSON and endpoint URL
    return jsonify({'questions': json_quiz})


@app.route('/logout')
def logout():
    ''' end and clear sessions for logged in users '''
    # clear the sessions
    session.clear()
    return redirect(url_for('login'))


@app.route('/delete_acct')
def delete_acct():
    ''' route to warning page '''
    return render_template('delete_acct.html')


@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    """Delete user account"""
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    try:
        
        # Delete user's attempted quizzes from quiz_attempted table
        cursor.execute("DELETE FROM quiz_attempted WHERE user_id = %s", (user_id,))

        # Delete user's quiz scores from quiz_scores table
        cursor.execute("DELETE FROM quiz_scores WHERE user_id = %s", (user_id,))

        # Delete user from users table
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

        # Commit the transactions
        db.commit()

        # Clear the session
        session.clear()

        return redirect(url_for('login'))
    except Exception as e:
        # If an error occurs, rollback changes and render an error message
        db.rollback()
        return render_template('delete_acct.html', error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
