#from crypt import methods
import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

# variable that controls the number of questions to be displayed per page
QUESTIONS_PER_PAGE = 10

# method to handle pagination of questions
def pagianate_questions(request, selection):
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

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs --DONE
    """
    CORS(app, resources={r"/api/*":{"origin":"*"}})
    

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow --DONE
    """
    #CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests --DONE
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        #fetches all categories by id
        categories = Category.query.order_by(Category.id).all()

        categories_obj = {}

        if len(categories) == 0:
            abort(404)
            
        for category in categories:
            categories_obj[category.id] = category.type

        return jsonify({
            'success':True,
            'categories' : categories_obj,
            })
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,     --DONE
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = pagianate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()

        categories_obj = {}

        if len(categories) == 0:
            abort(404)
            
        for category in categories:
            categories_obj[category.id] = category.type

        return jsonify({
            'success':True,
            'questions' : current_questions,
            'total_questions':len(Question.query.all()),
            'currentCategory': Category.query.get(current_questions[1]['category']).type,
            'categories': categories_obj
            })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID. --DONE       

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>',methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            
            question.delete()

            selection = Question.query.order_by(Question.id).all()
            current_questions = pagianate_questions(request, selection)


            return jsonify({
                'success':True,
                'deleted':question_id,
                'questions': current_questions,
                'total_questions':len(Question.query.all())
            })

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question, -- DONE
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        # gets the json attached to the request body 
        body = request.get_json()

        # extracts attribute data needed to create the question
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty_score = body.get('difficulty', None)

        try:
            # creates an instance of the question  
            question =  Question(question=new_question, answer=new_answer, category=new_category, difficulty = new_difficulty_score)

            # inserts into the database
            question.insert()

            # fetches all questions including the newly inserted question 
            selection = Question.query.order_by(Question.id).all()

            # calls the method to paginate and format and collate questions
            current_questions = pagianate_questions(request, selection)

            return jsonify({
                'success':True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """


    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        # gets the json attached to the request body 
        body = request.get_json()

        
        # extracts the search term
        search_word = body.get('searchTerm', None)

        # prepares/formats the search term for DB query usage
        formatted_search_word = "%{}%".format(search_word)

        try:
            # queries the database column based on the formatted search term 
            query_results = Question.query.filter(Question.question.ilike(formatted_search_word))

            # paginate/prepares the query results
            formatted_search_result = pagianate_questions(request, query_results)



            return jsonify({
                'success':'True',
                'search_term': search_word,
                'questions': formatted_search_result,
                'totalQuestions':len(formatted_search_result),
                'currentCategory': 'Entertainment'
            })

        except:
            abort(422)



    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):

        # queries the question DB table column based on the category ID
        selection = Question.query.filter_by(category = category_id).order_by(Question.id)

        # paginate/prepares the query results for frontend usage
        category_questions = pagianate_questions(request, selection)

        # validation to check if there isn't a category with that id --thereby making the query value empty
        if len(category_questions) == 0:
            abort(404)

        return jsonify({
            'success':True,
            'questions': category_questions,
            'totalQuestions':len(category_questions),
            'currentCategory': Category.query.get(category_id).type,
        })




    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz. ---DONE
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        # gets the json attached to the request body
        body = request.get_json()

        # extracts attribute data needed to generate the next question
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        print(quiz_category)

        try:
            # validate that the previous_question isn't empty
            if previous_questions is None:
                abort(404)

            # validate that the quiz_category isn't empty
            if quiz_category is None:
                abort(404)

            # extracts the category id 
            category_id = quiz_category["id"]

            # queries the question DB table where the category = category_id and question.id is not in previous_questions
            questions = Question.query.filter(Question.category == category_id , ~Question.id.in_(previous_questions))

            # formats the query results
            formatted_questions = [question.format() for question in questions]

            #selects a random question from the query results
            current_question = random.choice(formatted_questions)

            return jsonify({
                'success':True,
                'question' : current_question,
            })
        except:
            abort(422)


                


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message":"resource not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success":False,
            "error":422,
            "message":"unprocessable"
        }), 422


    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success":False,
            "error":500,
            "message":"Internal Server Error"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False,
           "error": 400, 
           "message": "bad request"
           }), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False,
             "error": 405, 
             "message": "method not allowed"}),
            405,
        )

    return app

