# The Ultimate Udacity Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method Not Allowed
- 500: Internal Server Error  

### Endpoints 
#### GET /categories
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
    - Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### GET /questions?page=${integer}
- General:
    - Fetches a paginated set of questions, a total number of questions, all categories and current category string.
    - Request Arguments: `page` - integer
    - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string 
    - Sample: `curl http://127.0.0.1:5000/questions?page=1`

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

#### GET /categories/${id}/questions
- General:
    - Fetches questions for a cateogry specified by id request argument
    - Request Arguments: `id` - integer
    - Returns: An object with questions for the specified category, total questions, and current category string
- `curl http://127.0.0.1:5000/categories/3/questions`

```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```
#### DELETE /questions/${question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total question.
- `curl -X DELETE http://127.0.0.1:5000/questions/4`
```json
  {
    "deleted": 26,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        
    ],
    "success": true,
    "total_questions": 19
}
```

#### POST /question
- General:
    - Creates a new question using the submitted question, category, answer and difficulty. Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend. 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{"question":"Who is the current coach of Manchester United football club","answer":"Erik Ten Hag","category":6,"difficulty":3}"`
```json
{
  "questions": [
    {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "created": 24,
  "success": true,
  "total_questions": 30
}
```

#### POST /question/search
- General:
    - Sends a post request in order to search for a specific question by search term
- `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d "{"searchTerm": "title"}"`
```{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 5
        },
    ],
    "totalQuestions": 100,
    "currentCategory": "Entertainment"
}
```

#### POST /quizzes
- General:
    - Sends a post request in order to get the next question
    - Returns a single new question object
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d "{"previous_questions": [1, 4, 20, 15], "quiz_category": {type:"science",id:1}}"`
```{
    "question": {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 4
    }
}
```


## Deployment N/A

## Authors
Yours truly, Akindolie, Michael Akinloye 

## Acknowledgements 
The awesome team at Udacity and ALX-T ....Kudos! 

