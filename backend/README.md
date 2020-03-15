# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Endpoints
Endpoints
GET '/categories'
GET ‘/questions’
DELETE '/questions/<question_id>'
POST '/questions'
GET '/categories/<category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of questions with pagination of 10 questions every page 
- Request Arguments: integer indicates which page of questions to show 
'/questions?page=1'
- Returns: An object with multiple key-value pairs including 1). 'questions': a list of paginated questions where each question is also an object with multiple key-value pairs including question id, question description, difficulty of the question and the category of the question. 2). 'total_question': total number of questions 3). 'categorys': An object with a single key, categories, that contains a object of id: category_string key:value pairs. 4). 'current_caetory': the category of the first shown question 
{'questions' : [{'id': 1, 'question': '...', 'answer': '...', 'category':1, 'difficulty': 1}, {...}, ...],
'total_questions': 19,
'categories': {'1' : "Science", '2' : "Art", ... }
'current_category': 1
}

DELETE '/questions/<question_id>'
- Delete a question based on the question id in URL
- Request Arguments: question id in the URL
'/questions/1'
- Returns: An object with a single key-value pair 'success': True when the operation succeeds
{'success': True}

POST '/questions'
- Create a new question or seach for questions. Question creation will take the question id, question description, the answer to it, the difficulty and the category of the question. Question serching will search for all the questions contianing the search term as sub string in the quesiton. Which action to take is dependant on parsing the request arguments
- Request Arguments: 1). create a new question: a json object with multiple key-value pairs including question id, question description, difficulty of the question and the category of the question. 
{'id': 1, 'question': '...', 'answer': '...', 'category':1, 'difficulty': 1}
2). a json object with a single key-value pair including the search term, note the seaching is case insensitive 
{'searchTerm': '...'}
- Returns: 1). create a new question: An object with a single key-value pair 'success': True when the operation succeeds
{'success': True}
2). search quesitons: An object with multiple key-value pairs including 1). 'questions': a list of matched questions where each question is also an object with multiple key-value pairs including question id, question description, difficulty of the question and the category of the question. 2). 'total_question': total number of matched questions  3). 'current_caetory': the category of the first shown question 
{'questions' : [{'id': 1, 'question': '...', 'answer': '...', 'category':1, 'difficulty': 1}, {...}, ...],
'total_questions': 2,
'current_category': 1
}

GET '/categories/<category_id>/questions'
- Fetches a list of questions belongs to a specific category
- Request Arguments: catory id indicating questions of which category to be shown  
'categories/1/questions'
- Returns: An object with multiple key-value pairs including 1). 'questions': a list of questions within the specific category where each question is also an object with multiple key-value pairs including question id, question description, difficulty of the question and the category of the question. 2). 'total_question': total number of questions within the specific category  3). 'current_caetory': the category of the result questions
{'questions' : [{'id': 1, 'question': '...', 'answer': '...', 'category':1, 'difficulty': 1}, {...}, ...],
'total_questions': 4,
'current_category': 2
}

POST '/quizzes'
- Return a new randomly picked question with the same category of the previous questions but different from them
- Request Arguments: json object with two key value pairs including 1). a list of previous questions' id  2). an obejct with a single key-value pair indicating the category id and its corresponding category 
{'previous_questions': [1, 2, 3], 'quiz_category': {1: 'Science'}}
- Return: an object with multiple single key-value pair containing the randomly picked question which is a multiple key-value pairs including question id, question description, difficulty and the category of the question.
{'questions' : {'id': 1, 'question': '...', 'answer': '...', 'category':1, 'difficulty': 1}}

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```