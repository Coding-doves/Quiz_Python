import random
import requests
import json


class Quiz:
    def __init__(self, api_url):
        ''' intializing question and the dafault score'''
        self.api_url = api_url
        self.questions = self.fetch_quiz()
        self.score = 0

    def fetch_quiz(self):
        '''fetch questions from the API'''
        question_option = []

        try:
            response = requests.get(self.api_url)
            response.raise_for_status()  # Raise an error for unsuccessful status codes
            if response.status_code == 200:
                # API Response
                api_response = response.json()
                # print("API Response:", api_response)
                # get question from API Response
                for data in api_response:
                    question = data.get("question", {}).get("text")
                    correct_ans = data.get("correctAnswer")
                    incorrect_ans = data.get("incorrectAnswers", [])
                    
                    options = [correct_ans] + incorrect_ans
                    random.shuffle(options)

                    question_data = {
                        "question": question,
                        "options": options,
                        "answer": correct_ans
                    }

                    question_option.append(question_data)
                
                return question_option
            
        except requests.exceptions.RequestException as e:
            print("Failed to fetch questions from the API:", e)
            return {}

    ''' display for the console only'''
    def display_quiz(self, que, ans):
        '''prints questions with options to the console'''
        print(que)
        for i, a in enumerate(ans):
            print(f'- {a}')

    def check_ans(self, usr_inpt, correct_ans):
        ''' checking if user enter the correct answer'''
        return usr_inpt.lower() == correct_ans.lower()

    def run_quiz(self):
        '''run quiz questions on the console only'''
        if not self.questions:
            print("No questions available at this time.")
            return
        
        # convert data to list before using random(takes sequence/list)
        random.shuffle(self.questions)

        for data in self.questions:
            question = data['question']
            option = data['options']
            correct = data['answer']

            self.display_quiz(question, option)
            user_input = input('Enter answer: ')

            if self.check_ans(user_input, correct):
                self.score += 1
        
        print(f"You scored {self.score} out of {len(self.questions)}.")

# api endpoint
api_url = "https://the-trivia-api.com/v2/questions"

# create Quiz instance
# quiz_console = Quiz(api_url)
# run quiz
# quiz_console.run_quiz()
