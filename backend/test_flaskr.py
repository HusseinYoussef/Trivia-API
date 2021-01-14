import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Question, Category
from config import setup_db


class CategoryTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        setup_db(self.app, env='test')
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_success_get_categories(self):
        res = self.client().get('/v1/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))


class QuestionTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        setup_db(self.app, env='test')
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_success_get_questions(self):
        res = self.client().get('/v1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_get_questions_pagination_if_no_page(self):
        res = self.client().get('/v1/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_success_delete_question(self):
        res = self.client().delete('/v1/questions/9')
        data = json.loads(res.data)

        ques = Question.query.get(9)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(ques, None)
        self.assertEqual(data['deleted_id'], 9)

    def test_404_delete_question_if_no_question(self):
        res = self.client().delete('/v1/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_success_add_question(self):
        res = self.client().post('/v1/questions', json={
                                'question': 'Is Flask hard to learn?',
                                'answer': 'Not at all',
                                'difficulty': 1,
                                'category': 1
                            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_400_add_question_if_miss_parameters(self):
        res = self.client().post('/v1/questions', json={
                                'question': 'What is your name?',
                                'difficulty': 1,
                                'category': 2
                            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad Request")

    def test_search_question_with_results(self):
        res = self.client().post('/v1/questions', json={
                                    'searchTerm': 'title'
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_404_question_without_results(self):
        res = self.client().post('/v1/questions', json={
                                    'searchTerm': 'Dinosaurs'
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_success_get_category_questions(self):
        res = self.client().get('/v1/categories/1/questions')
        data = json.loads(res.data)

        category = Category.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], category.type)

    def test_404_get_category_questions_if_no_category(self):
        res = self.client().get('/v1/categories/50/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_success_quiz(self):
        ids = [16, 17]
        res = self.client().post('/v1/quizzes', json={
                                    'previous_questions': ids,
                                    'quiz_category': {'id': 2, 'type': 'Art'}
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 2)
        self.assertTrue(data['question']['id'] not in ids)

    def test_400_quiz_if_miss_parameters(self):
        res = self.client().post('/v1/quizzes', json={
                                'quiz_category': {'id': 1, 'type': 'Science'}
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
