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
        self.database_path = "postgresql://{}:{}@{}/{}".format('yaser', 'yaser','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'How many Ballon d’Or has Lionel Messi has earned?',
            'answer': 'Messi earned six Ballon d’Or',
            'difficulty': 2,
            'category': '6'
        }

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
    test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_categories(self):
        res = self.client().get('/categories')
        if res.status_code != 200:
            print('API endpoint Not Found...')
            self.assertEqual(res.status_code, 404)
        else:
            data =  json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['total_Categories'])
            self.assertTrue(len(data['Categories']))
    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valid_page(self):
        """Tests question pagination failure 404"""

        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
        
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['total_questions'], int)
        self.assertEqual(data['current_category'], data['current_category'])
        for question in data['questions']:
            self.assertEqual(int(question['category']), 1)
    
    def test_422_get_questions_by_category_fail(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        if res.status_code != 200:
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'Unprocessable')
        else:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], 2)
            self.assertTrue(data['total_questions'])
            self.assertTrue(len(data['questions']))
            self.assertEqual(question, None)
    
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
    
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
    
    def test_search_questions(self):
        """Tests search questions success"""
        res = self.client().post('/questions/search', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        if data['success']== False:
            self.assertEqual(res.status_code, 404)
        else:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['total_questions'])
            self.assertTrue(len(data['questions']))
    
    def test_404_if_search_questions_fails(self):
        """Tests search questions failure 404"""
        searchTerm_invalid = {'searchTerm': 'searchQuestionsFails' }
        searchTerm_empty = {'searchTerm': ' '}
        
        res = self.client().post('/questions/search', json=searchTerm_invalid or searchTerm_empty)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
    
    def test_play_the_quiz(self):
        res = self.client().post('/quizzes', json={
            'quiz_category': {
                'type': 'Sports',
                'id': 6
            },'previous_questions': [10, 11],
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 6)
        self.assertNotEqual(data['question']['id'], 10)
        self.assertNotEqual(data['question']['id'], 11)
    
    def test_play_the_quiz_fail(self):
        test_data = {}
        res = self.client().post('/quizzes', json=test_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()