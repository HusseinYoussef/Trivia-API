# Full Stack Trivia

Trivia is a web app that consists of a webpage to manage the app and a restful api to provide the app with different data including categories and questions.

## Functionalities

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started
### Frontend
### Installing Dependencies

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

### Backend
### Installing Dependencies
```bash
pip install -r requirements.txt
```
### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
### Running the server
From within the `backend` directory.

To run the server, execute:
```
python app.py
```
### Tests
To run the tests, run
```
drop database trivia_test;
create database trivia_test;
psql trivia_test < trivia.psql
python test_flaskr.py
```
Omit the drop command the first time you run tests (since the database doesn't exist).
## API Reference
### Getting Started
* Base URL: Currently this application is only hosted locally. The backend is hosted at http://127.0.0.1:5000/
* Authentication: This version does not require authentication or API keys.

### Error Handling
Errors are returned as JSON in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "Bad Request"
}
```
The API will return three types of errors:

* 400 – Bad Request
* 404 – Not Found
* 405 – Method not allowed
* 422 – Unprocessable

### Endpoints
#### GET /v1/categories
* General: Return list of objects of all available categories.
* Sample: ```curl -X GET http://127.0.0.1:5000/v1/categories``` <br>

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### GET /v1/questions
* General:
    * Return list of all question objects, number of questions and list of categories.
    * Results are paginated in groups of 10. Include a request argument to choosee page number, starting from 1.
* Sample: `curl -X GET http://127.0.0.1:5000/v1/questions`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```
#### DELETE /v1/questions/{question_id}
* General: 
    * Delete a question by id.
    * Returns the id of the deleted question in case of success.
* Sample: `curl -X DELETE http://127.0.0.1:5000/v1/questions/2`
```
{
  "deleted_id": 14,
  "success": true
}
```

#### POST /v1/questions
* General: 
  * Create a new question using JSON body.
  * Return the newly create question id and total number of questions.
* Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"question\" :\"is flask hard\", \"answer\":\"Not at all\", \"difficulty\":\"1\", \"category\":\"1\"}" http://127.0.0.1:5000/v1/questions`
```
{
  "created_id": 24,
  "success": true,
  "total_questions": 19
}
```

*Note: if searchTerm is included:*
* General:
  * Search for matching questions.
  * Return matching questions if found and their number.
* Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"searchTerm\" :\"title\"}" http://127.0.0.1:5000/v1/questions`

```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### GET /v1/categories/{category_id}/questions
* General:
  * Get question of a specific category by id.
  * Return paginated questions of that catefory and the name of the category.
* Sample: `curl -X GET http://127.0.0.1:5000/v1/categories/1/questions`

```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Not at all",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "is flask hard"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### POST /v1/quizzes
* General: 
  * Use previous_questions and category parameters.
  * Return a random question of that category, and that is not one of the previous questions.
* Sample: `curl -X POST -H "Content-Type: application/json" -d "{\"previous_questions\": [24,21], \"quiz_category\":{\"id\":1, \"type\": \"Science\"}}" http://127.0.0.1:5000/v1/quizzes`

```
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```
## Authors
All other project files, including the models and frontend, were created by Udacity as a project template for the Full Stack Web Developer Nanodegree.
