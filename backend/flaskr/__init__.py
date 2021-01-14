import os
from flask import Flask, request, abort, jsonify, Response
from flask_cors import CORS
import random

from models import Question, Category
from config import setup_db

QUESTIONS_PER_PAGE = 10

# Codes
Ok = 200
Created = 201
Bad_request = 400
Not_found = 404
Method_not_allowed = 405
Not_processable = 422


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
                    'Allow-Control-Allow-Headers',
                    'Content-Type,Authorization,true'
                    )
        response.headers.add(
                    'Allow-Control-Allow-Methods',
                    'GET, POST, DELETE, OPTIONS'
                    )

        return response

    @app.route('/v1/categories', methods=['GET'])
    def get_all_categories():

        categories = Category.query.all()

        if len(categories) == 0:
            abort(Not_found)

        # Create dictionary for categories {id -> type}
        data = {cate.id: cate.type for cate in categories}
        return jsonify({
                "success": True,
                "categories": data
            }), Ok

    @app.route('/v1/questions', methods=['GET'])
    def get_all_question():

        questions = Question.query.order_by(Question.id).all()
        # get page of questions
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE

        questions_page = Question.query.order_by(
                                Question.id
                                ).limit(QUESTIONS_PER_PAGE).offset(start).all()

        categories = Category.query.all()
        categories_data = {cate.id: cate.type for cate in categories}

        # not found if no question or cateqories
        if len(questions) == 0 or len(categories) == 0\
                or len(questions_page) == 0:
            abort(Not_found)

        return jsonify({
            "success": True,
            "questions": [q.format() for q in questions_page],
            "total_questions": len(questions),
            "categories": categories_data
        }), Ok

    @app.route('/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(Not_found)

        try:
            question.delete()
        except Exception as e:
            # not processable if can't delete the question
            print(e)
            abort(Not_processable)

        return jsonify({
            'success': True,
            'deleted_id': question_id
        }), Ok

    @app.route('/v1/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        search_term = body.get('searchTerm', None)
        if search_term:

            # search for questions that has the search term (case insensitive)
            page = request.args.get('page', 1, type=int)
            start = (page-1)*QUESTIONS_PER_PAGE
            questions = Question.query.filter(
                                    Question.question.ilike(f'%{search_term}%')
                                    ).order_by(
                                        Question.id
                                        ).limit(
                                            QUESTIONS_PER_PAGE
                                            ).offset(start).all()
            # not found if no questions
            if len(questions) == 0:
                abort(Not_found)

            return jsonify({
                'success': True,
                'questions': [q.format() for q in questions],
                'total_questions': len(questions)
            }), Ok

        else:
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            # bad request if one of the required fields is missing
            if (question is None) or (answer is None) or\
                    (difficulty is None) or (category is None):
                abort(Bad_request)

            new_question = Question(
                                    question=question,
                                    answer=answer,
                                    difficulty=difficulty,
                                    category=category
                                )

            try:
                new_question.insert()
            except Exception as e:
                # not processable if can't insert the question
                print(e)
                abort(Not_processable)

            questions = Question.query.all()

            return jsonify({
                'success': True,
                'created_id': new_question.id,
                'total_questions': len(questions)
            }), Created

    @app.route('/v1/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):

        category = Category.query.get(category_id)

        if category is None:
            abort(Not_found)

        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE

        # get all question of that category
        questions = Question.query.filter(
                                Question.category == category_id
                                ).order_by(
                                    Question.id
                                    ).limit(
                                        QUESTIONS_PER_PAGE
                                        ).offset(start).all()

        if len(questions) == 0:
            abort(Not_found)

        return jsonify({
            'success': True,
            'questions': [q.format() for q in questions],
            'total_questions': len(questions),
            'current_category': category.type
        }), Ok

    @app.route('/v1/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        # get the required parameters
        previous_questions = body.get('previous_questions', None)
        category = body.get('quiz_category', None)

        # Bad request if one of the required parameter is none
        if (previous_questions is None) or (category is None):
            abort(Bad_request)

        # get all question if id is 0
        if category['id'] == 0:
            questions = Question.query.all()
        # get all question of quiz category
        else:
            questions = Question.query.filter(
                                        Question.category == category['id']
                                        ).all()

        if len(questions) == 0:
            abort(Not_found)

        if len(previous_questions) >= len(questions):
            return jsonify({
                'success': True,
                'message': "No more questions"
            }), Ok

        import numpy as np
        # make number of trials to avoid infinite loop
        trials = 0
        while trials <= 100:
            chosen_question = np.random.choice(questions, replace=True)
            if not(chosen_question.id in previous_questions):
                break
            trials += 1

        if trials > 100:
            abort(Not_found)

        return jsonify({
            'success': True,
            'question': chosen_question.format()
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error_code': Bad_request,
            'message': "Bad Request"
        }), Bad_request

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Not Found",
            "error_code": Not_found
        }), Not_found

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "message": "Method not Allowed",
            "error_code": Method_not_allowed
        }), Method_not_allowed

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            'success': False,
            'error_code': Not_processable,
            'message': "Cannot be processed"
        }), Not_processable

    return app
