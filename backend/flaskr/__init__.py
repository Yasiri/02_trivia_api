import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category
from random import randrange

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @cors Set up CORS. Allow '*' for origins.
    '''
    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
    '''
   after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories')
    def get_all_categories():
        try:
            selection = Category.query.order_by(Category.id).all()
            categories_list = {}

            for category in selection:
                categories_list[category.id] = category.type

            if len(categories_list) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'Categories': categories_list,
                'total_Categories': len(Category.query.all())
            })
        except Exception:
            abort(422)

    '''
    An endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint returns:
    list of questions, number of total questions, current category, categories.
    '''

    @app.route('/questions', methods=['GET'])
    def get_all_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
            current_questions = paginate_questions(request, questions)

            category_list = {}

            for category in categories:
                category_list[category.id] = category.type

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': category_list
            })
        except Exception:
            abort(404)

    '''
    An endpoint to DELETE question using a question ID.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(
              Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_question,
                'total_questions': len(Question.query.all())
            })
        except Exception:
            abort(422)

    '''
    An endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    '''

    @app.route('/questions', methods=['POST'])
    def create_questions():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(
              question=new_question, answer=new_answer,
              difficulty=new_difficulty, category=new_category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_question = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'question_created': question.question,
                'questions': current_question,
                'total_questions': len(Question.query.all())
            })
        except Exception:
            abort(422)

    '''
    A POST endpoint to get questions based on a search term.
    It returns any questions for whom the search term
    is a substring of the question.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm')

            if body is None or search_term == ' ':
                abort(404)
            else:
                search_term = body.get('searchTerm')
                selection = Question.query.filter(
                  Question.question.ilike(f'%{search_term}%')).all()

            if (len(selection) == 0):
                abort(404)

            paginated = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(paginated)
            })
        except Exception:
            abort(404)

    '''
    A GET endpoint to get questions based on category.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_based_on_category(category_id):
        try:
            category_type = Category.query.filter_by(
              id=category_id).one_or_none()

            if category_type is None:
                abort(400, 'Invalid category id')

            selection = Question.query.filter(
              Question.category == str(category_type.id)).all()
            questions = paginate_questions(request, selection)

            return jsonify({
                'Success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': category_type.type,
                'current_category_id': category_type.id
            })
        except Exception:
            abort(422)

    '''
    A POST endpoint to get questions to play the quiz.
    This endpoint takes category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_the_quiz():
        try:
            body = request.get_json()  # get request body
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            if quiz_category['type'] == 'click':
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                  category=quiz_category['id']).all()

            next_question = questions[randrange(0, len(questions))]

            for q in previous_questions:
                next_question = questions[randrange(0, len(questions))]

            return jsonify({
                'success': True,
                'question': next_question.format(),
            }), 200
        except Exception:
            abort(400)

    '''
    Error handlers for all expected errors
    including 404, 422, 400 and 500.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(500)
    def internal_server_error_500(e):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    return app
