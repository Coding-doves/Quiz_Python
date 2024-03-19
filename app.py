from flask import Flask, render_template
from quiz import Quiz

app = Flask(__name__)


@app.route('/')
def index():
    ''' output to browser '''
    # api endpoint
    api_url = "https://the-trivia-api.com/v2/questions"

    # create Quiz instance
    quiz = Quiz(api_url)
    # print("Quiz Questions:", quiz.questions)
    return render_template('index.html', questions=quiz.questions)


if __name__ == '__main__':
    app.run(debug=True)
