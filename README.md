**Quiz App**

---

### Overview

The Quiz App is a web application designed to allow users to take quizzes on various topics. Users can register an account, login, take quizzes, view their quiz history, and manage their profile details.

### Features

- User authentication: Users can register an account and log in securely.
- Quiz taking: Users can take quizzes on different topics.
- Quiz history: Users can view their quiz history and scores.
- Profile management: Users can update their profile details and images.

### Technologies Used

- Python
- Flask
- MySQL
- bcrypt (for password hashing)
- Jinja2 (for templating)
- HTML/CSS/JavaScript (for front-end)

### Getting Started

1. Clone the repository:

```
git clone https://github.com/Coding-doves/Quiz_Python.git
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Set up MySQL database:

   - Create a MySQL database named `quizapp`.
   - Update the database connection settings in `app.py` to match your MySQL configuration.

4. Run the application:

```
python app.py
```

5. Open your web browser and navigate to `http://localhost:5000` to access the Quiz App.

### Usage

- **Registration:** Navigate to the registration page (`/signup`) to create a new account.
- **Login:** Log in with your username and password on the login page (`/login`).
- **Quiz Taking:** Take quizzes on various topics by visiting the quiz page (`/quiz`).
- **View Quiz History:** Check your quiz history and scores on the dashboard (`/dashboard`).
- **Profile Management:** Update your profile details and images on the profile page (`/profile`).

## API Documentation Quiz Attempted Questions

This API documentation provides details on the Quiz App API endpoints for retrieving 20 recently attempted quiz data.

### Questions API
---
Extration from [Trivia](https://the-trivia-api.com/v2/questions)

### Endpoint: /questions
- Method: GET
- Description: Retrieve recent quiz questions and answers for the logged-in user.
- Authentication: Requires user to be logged in.
- Response:
  - Status Code: 200 OK
  - Content Type: application/json
  - Body: 
    ```
    {
        "json_quiz": [
            {
                "id": null,  // Assuming there's no ID for each question in the database
                "text": "Question text",
                "answers": [
                    {"id": null, "text": "User's answer", "correct": true/false},  // User's answer
                    {"id": null, "text": "Correct answer", "correct": true}  // Correct answer
                ]
            },
            ...
        ]
    }
    ```

### ICONS from www.flaticon.com and https://iconscout.com
- <a href="https://www.flaticon.com/free-icons/info" title="info icons">Info icons created by Chanut - Flaticon</a>
- https://www.flaticon.com/authors/sumberrejeki/basic-outline?author_id=917&type=standard
- https://www.flaticon.com/authors/freepik
- <a href="https://www.flaticon.com/free-icons/quizzes" title="quizzes icons">Quizzes icons created by small.smiles - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/dashboard" title="dashboard icons">Dashboard icons created by Pixel perfect - Flaticon</a>
- https://iconscout.com/contributors/icon-mafia
- https://iconscout.com/contributors/unicons

### Contributions

Contributions to the Quiz App are welcome! If you find any bugs or have suggestions for improvement, please feel free to open an issue or submit a pull request.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.

### Contact

For any inquiries or support, please contact [Ada](mailto:obenedicta4@gmail.com).

---

This README provides an overview of the Quiz App, including its features, technologies used, setup instructions, usage guide, API documentation, contributions, license, and contact information.
