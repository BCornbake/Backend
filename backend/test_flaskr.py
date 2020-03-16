import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        def tearDown(self):
            """Executed after reach test"""
            pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """
    # test case for showing available categories
    def test_show_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        category_query = Category.query.all()
        self.assertEqual(res.status_code, 200)
        for category in category_query:
            self.assertEqual(
                data['categories'][str(category.id)],
                category.type
            )

    # test case for showing paginated questions
    def test_show_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    # test case for 404 when page number is too large
    def test_404_for_invalid_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    # test case for delete a question
    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # test case for delete an invalid question
    def test_404_for_delete_question(self):
        res = self.client().delete('/question/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    # test case for create a new question
    def test_create_question(self):
        res = self.client().post('/questions', json={
            'id': 88,
            'question': 'Who is the first chinese emperor?',
            'answer': 'Ying Zheng',
            'difficulty': 3,
            'category': 4
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # test case for create a new question with unprocessable entity
    def test_422_for_create_question(self):
        res = self.client().post('/questions', json={
            'id': 89,
            'question': 'Who is the first chinese emperor?',
            'answer': 'Ying Zheng',
            'difficulty': 3,
            'category': 8
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(
            data['message'],
            'correct request format, but unprocessable entity'
            )

    # test case for search question
    def test_search_question(self):
        res = self.client().post('/questions', json={
            'searchTerm': 'title'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # test case for no search result
    def test_422_search_question(self):
        res = self.client().post('/questions', json={
            'searchTerm': 'tttiekg'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(
            data['message'],
            'correct request format, but unprocessable entity'
            )

    # test case for show questions based on category
    def test_show_category_question(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['currrent_category'])

    # test case for show questions based on invalid category
    def test_show_category_question(self):
        res = self.client().get('/categories/100questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    # test case for playing quiz
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 4, 'type': 'History'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    # test case for playinf quiz with wrong request format
    def test_400_for_play_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': 4
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'wrong request format')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
