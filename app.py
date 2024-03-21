from flask import Flask, render_template, request
import bcrypt
import mysql.connector
from quiz import Quiz
import random

app = Flask(__name__)

# Connect to mysql db
db = mysql.connector.connect(
    host='localhost',
    user='dove',
    password='password',
    database='QuizApp'
)
cursor =db.cursor()


@app.route('/')
def index():
    ''' output to browser '''
    # api endpoint
    api_url = "https://the-trivia-api.com/v2/questions"

    # create Quiz instance
    quiz = Quiz(api_url)
    random.shuffle(quiz.questions)
    # print("Quiz Questions:", quiz.questions)
    return render_template('index.html', questions=quiz.questions)


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


if __name__ == '__main__':
    app.run(debug=True)
