import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app)
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type, Authorization'
          )
        response.headers.add(
          'Access-Control-Allow-Methods',
          'GET, POST, PATCH, DELETE, OPTIONS'
          )
        return response
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def show_categories():
        categories = {}
        results = Category.query.order_by("id").all()
        for result in results:
            categories[result.id] = result.type
        return jsonify({
          "categories": categories
        })
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route("/questions", methods=['GET'])
    def show_questions():
        try:
            page = request.args.get('page', 1, type=int)
        except:
            abort(400)
        question_query = Question.query.order_by("id").all()
        category_query = Category.query.order_by("id").all()
        max_page = round(len(question_query)/QUESTIONS_PER_PAGE+0.4)
        if page > max_page:
            abort(404)
        try:
            start = (page-1)*QUESTIONS_PER_PAGE
            end = min(
              (page-1)*QUESTIONS_PER_PAGE+QUESTIONS_PER_PAGE,
              len(question_query)
              )
            result_questions = question_query[start: end]
            questions = []
            for question in result_questions:
                temp = {}
                temp['id'] = question.id
                temp['question'] = question.question
                temp['answer'] = question.answer
                temp['category'] = question.category
                temp['difficulty'] = question.difficulty
                questions.append(temp)
            total_questions = len(question_query)
            categories = {}
            for category in category_query:
                categories[category.id] = category.type
            current_category = Category.query.filter_by(
              id=question_query[0].category).first().id
            return jsonify({
              "questions": questions,
              "total_questions": total_questions,
              "categories": categories,
              "current_category": current_category
              })
        except:
            abort(500)
    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        error = 0
        try:
            question = Question.query.get(question_id)
            db.session.delete(question)
            db.session.commit()
        except:
            error = 1
            db.session.rollback()
        finally:
            db.session.close()
        if error == 0:
            return jsonify({
              "success": True
            })
        else:
            abort(404)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page of the questions list
    in the "List" tab.
    '''
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions', methods=['POST'])
    def create_search_question():
        try:
            request_text = request.get_json()
        except:
            abort(400)
        try:
            if 'searchTerm' in request_text:
                search_term = request_text['searchTerm']
            else:
                id = request_text['id']
                question = request_text['question']
                answer = request_text['answer']
                difficulty = request_text['difficulty']
                category = request_text['category']
        except:
            bort(422)
        error = 0
        # in the case of searching question
        if 'searchTerm' in request_text:
            result = Question.query.filter(Question.question.ilike(
              f'%{search_term}%')).order_by(Question.id).all()
            if len(result):
                questions = []
                for question in result:
                    temp = {}
                    temp['id'] = question.id
                    temp['question'] = question.question
                    temp['answer'] = question.answer
                    temp['category'] = question.category
                    temp['difficulty'] = question.difficulty
                    questions.append(temp)
                total_questions = len(questions)
                current_category = result[0].category
                return jsonify({
                  "questions": questions,
                  "total_questions": total_questions,
                  "current_category": current_category
                })
            else:
                abort(422)
        # in the case of creating a new question
        else:
            try:
                question_ins = Question(
                  question=question, answer=answer,
                  difficulty=difficulty, category=category
                  )
                db.session.add(question_ins)
                db.session.commit()
            except:
                error = 1
                db.session.rollback()
            finally:
                db.session.close()
            if error:
                abort(422)
            else:
                return jsonify({
                  'success': True
                })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def show_questions_on_category(category_id):
        try:
            questions_query = Question.query.filter_by(
              category=category_id).all()
        except:
            abort(404)
        if len(questions_query):
            questions = []
            for question in questions_query:
                temp = {}
                temp['id'] = question.id
                temp['question'] = question.question
                temp['answer'] = question.answer
                temp['category'] = question.category
                temp['difficulty'] = question.difficulty
                questions.append(temp)
            total_questions = len(questions_query)
            current_category = category_id
            return jsonify({
              "questions": questions,
              "total_questions": total_questions,
              "current_category": current_category
            })
        else:
            abort(500)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            request_text = request.get_json()
            pre_questions = request_text['previous_questions']
            quiz_category = request_text['quiz_category']
            category_id = quiz_category['id']
            category_type = quiz_category['type']
        except:
            abort(400)
        result_question = None
        try:
            questions = Question.query.filter_by(category=category_id).all()
            if pre_questions:
                for question in questions:
                    if question.id not in pre_questions:
                        result_question = question
            else:
                result_question = questions[0]
        except:
            abort(500)
        if not result_question:
            abort(422)
        else:
            question_result = {
              'id': result_question.id,
              'question': result_question.question,
              'answer': result_question.answer,
              'category': result_question.category,
              'difficulty': result_question.difficulty
              }
            return jsonify({'question': question_result})

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
          "error": 400,
          "message": "wrong request format"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "error": 404,
          "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
          "error": 422,
          "message": "correct request format, but unprocessable entity"
        }), 422

    @app.errorhandler(500)
    def unprocessable_entity(error):
        return jsonify({
          "error": 500,
          "message": "internal service error"
        }), 500

    return app
