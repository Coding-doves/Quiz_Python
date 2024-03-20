from flask import Flask, render_template, request
from quiz import Quiz
import random

app = Flask(__name__)


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

    for key, value in request.form.items():
        if key.startswith('opt'):
            que_index = key[3:] # Extract index of the question
            answer_key = 'correct' + que_index
            correct_ans = request.form.get(answer_key)
            
            if value == correct_ans:
                score += 1

    return render_template('result.html', score=score)


if __name__ == '__main__':
    app.run(debug=True)
