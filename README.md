# Trivia API Project - Udacity
 
 # Full Stack API Final Project
The trivia is a game that allow users to test their knowledge by playing a simple game of randomized questions. The goal of this project is to structure plan, implement, and test the API to Complete the trivia app. where the application must meet the following requirements:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

All backend codes follow [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)
## Getting Started
### Dependencies Installation:
Developers using this project should have Python3, pip3, nodeJS, and npm installed.

#### Installing Backend dependencies:
first create a virtual environment "when using Python for this projects". Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
This will install all the required packages we selected within the `requirements.txt` file.

#### Installing Frontend dependencies:
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

## Running the Server
From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
## Running the Frontend
The frontend app was built using create-react-app. To run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

```bash
npm start
```
Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

## APIs Testing:
To TEST the API End points, run the following commands:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Skip "dropdb trivia_test" command for the first time running the test.

# Reference
## Getting Started
* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, (http://127.0.0.1:5000/), which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
   'success': False,
   'error': 404,
   'message': 'Resource Not Found'
}
```

The API will return Four error types when requests fail:
* 404: Resource Not Found
* 422: Unprocessable
* 400: Bad request
* 500: Internal server error
There are `TODO` comments throughout project. Start by reading the READMEs in:

## Endpoints
### GET /categories
* General:
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
* Sample:
  - curl http://127.0.0.1:5000/categories
```
{
  '1' : "Science",
  '2' : "Art",
  '3' : "Geography",
  '4' : "History",
  '5' : "Entertainment",
  '6' : "Sports"
}
```
1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)

