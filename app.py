from flask import Flask, jsonify, render_template, request, redirect, url_for
import bcrypt
import mysql.connector
from quiz import Quiz
import random

app = Flask(__name__)

# Connect to mysql db
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Ada.070#X',
    database='QuizApp'
)
cursor =db.cursor()


@app.route("/", methods=['GET', 'POST'])
def login():
    """authenticating user """
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        passwd = data.get('password')

        query = "SELECT password FROM user WHERE username = %s"
        cursor.execute(query, (username,))
        value = cursor.fetchone()

        if value:
            hashed_password = value[0]
            if bcrypt.checkpw(passwd.encode('utf-8'), hashed_password.encode('utf-8')):
                # --- work on session for logged in user
                return redirect(url_for('quiz'))
            else:
                return render_template('login.html', message="Wrong password")
        else:
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
        query = 'INSERT INTO users (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)'
        cursor.execute(query, (firstname, lastname, username, hashed_passwd))
        db.commit()

        return redirect(url_for('login'))
    
    return render_template('signup.html')


@app.route('/quiz')
def quiz():
    ''' output to browser '''
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
    score = 0
    total_questions = int(request.form.get(total_questions))
    for key, value in request.form.items():
        if key.startswith('opt'):
            que_index = key[3:] # Extract index of the question
            answer_key = 'correct' + que_index
            correct_ans = request.form.get(answer_key)
            question = request.form.get('question' + que_index)

            # increase score by 1 for correct answer
            if value == correct_ans:
                score += 1

            # gather questions data for table display
            question_data = {
                'question': question,
                'user_answer': value,
                'correct_answer': correct_ans
            }

    return render_template('result.html',
        score=score,
        total_questions=total_questions,
        question_data=question_data)


@app.route('/logout')
def logout():
    ''' end and clear sessions for logged in users '''
    # -----work on clear the sessions
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
