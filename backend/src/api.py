"""Module for api."""

import json

from flask import Flask, abort, jsonify, request

from flask_cors import CORS

from .auth import AuthError, requires_auth
from .constants import (
    STATUS_BAD_REQUEST, STATUS_CODE_MESSAGES, STATUS_FORBIDDEN,
    STATUS_INTERNAL_SERVER_ERROR, STATUS_METHOD_NOT_ALLOWED,
    STATUS_NOT_FOUND, STATUS_UNAUTHORIZED, STATUS_UNPROCESSABLE_ENTITY
)
from .database import (
    Drink, add_new_drink, get_all_drinks, setup_db, update_drink_in_db
)
# from .database.models import db_drop_and_create_all

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"*": {"origins": "*"}})


@app.after_request
def after_request(response):
    """
    After request method to add cors.

    :param response:
    :return:
    """
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    )
    return response


"""
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
# db_drop_and_create_all()

# ROUTES


@app.route('/drinks')
def get_drinks():
    """
    Get drinks api with short detail.

    :return:
    """
    try:
        return jsonify({
            'success': True,
            'drinks': get_all_drinks()
        })
    except Exception as exp:
        abort(exp.code)


"""
@TODO implement endpoint
    GET /drinks-detail
    it should require the 'get:drinks-detail' permission
"""


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    """
    Get drinks api with long detail.

    :param token:
    :return:
    """
    try:
        return jsonify({
            'success': True,
            'drinks': get_all_drinks(is_short=False)
        })
    except Exception as exp:
        abort(exp.code)


"""
@TODO implement endpoint
    POST /drinks
    it should require the 'post:drinks' permission
"""


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(token):
    """
    Add new drink in the table.

    :param token:
    :return:
    """
    try:
        drink_data = request.get_json()
        drink_data['recipe'] = json.dumps(drink_data.get('recipe'))

        drink = add_new_drink(drink_data)
        return jsonify({
            'success': True,
            'drinks': [drink]
        })
    except Exception as exp:
        abort(exp.code)


"""
@TODO implement endpoint
    PATCH /drinks/<id> it should require the 'patch:drinks' permission
"""


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token, drink_id):
    """
    Update drink by given drink id.

    :param token:
    :param drink_id:
    :return:
    """
    try:
        drink = Drink.query.filter_by(id=drink_id).first()
        if not drink:
            abort(STATUS_NOT_FOUND)

        drink_data = request.get_json()
        drink_data['recipe'] = json.dumps(drink_data.get('recipe'))
        update_drink_in_db(drink, drink_data)
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as exp:
        abort(exp.code)


"""
@TODO implement endpoint
    DELETE /drinks/<id>
    it should require the 'delete:drinks' permission
"""


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):
    """
    Delete drink by given drink id.

    :param token:
    :param drink_id:
    :return:
    """
    try:
        drink = Drink.query.filter_by(id=drink_id).first()
        if not drink:
            abort(STATUS_NOT_FOUND)

        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except Exception as exp:
        abort(exp.code)


# Error Handling


@app.errorhandler(AuthError)
def auth_error(error):
    """
    Error handling for our custom auth error class.

    :param error:
    :return:
    """
    return jsonify(error.error), error.status_code


@app.errorhandler(STATUS_BAD_REQUEST)
def bad_request(error):
    """
    Error handler for bad request with status code 400.

    :param: error
    :return:
    """
    return jsonify({
        'success': False,
        'error': STATUS_BAD_REQUEST,
        'message': STATUS_CODE_MESSAGES[STATUS_BAD_REQUEST]
    }), STATUS_BAD_REQUEST


@app.errorhandler(STATUS_UNAUTHORIZED)
def unauthorized(error):
    """
    Error handler for unauthorized with status code 401.

    :param error:
    :return:
    """
    return jsonify({
        'success': False,
        'error': STATUS_UNAUTHORIZED,
        'message': STATUS_CODE_MESSAGES[STATUS_UNAUTHORIZED]
    }), STATUS_UNAUTHORIZED


@app.errorhandler(STATUS_FORBIDDEN)
def forbidden(error):
    """
    Error handler for forbidden with status code 403.

    :param error:
    :return:
    """
    return jsonify({
        'success': False,
        'error': STATUS_FORBIDDEN,
        'message': STATUS_CODE_MESSAGES[STATUS_FORBIDDEN]
    }), STATUS_FORBIDDEN


@app.errorhandler(STATUS_NOT_FOUND)
def not_found(error):
    """
    Error handler for not found with status code 404.

    :param error:
    :return:
    """
    return jsonify({
        'success': False,
        'error': STATUS_NOT_FOUND,
        'message': STATUS_CODE_MESSAGES[STATUS_NOT_FOUND]
    }), STATUS_NOT_FOUND


@app.errorhandler(STATUS_METHOD_NOT_ALLOWED)
def method_not_allowed(error):
    """
    Error handler for method not allowed with status code 405.

    :param error:
    :return:
    """
    return jsonify({
        'success': False,
        'error': STATUS_METHOD_NOT_ALLOWED,
        'message': STATUS_CODE_MESSAGES[STATUS_METHOD_NOT_ALLOWED]
    }), STATUS_METHOD_NOT_ALLOWED


@app.errorhandler(STATUS_UNPROCESSABLE_ENTITY)
def unprocessable_entity(error):
    """
    Error handler for unprocessable entity with status code 422.

    :param error:
    :return:
    """
    return jsonify({
        'success': False,
        'error': STATUS_UNPROCESSABLE_ENTITY,
        'message': STATUS_CODE_MESSAGES[STATUS_UNPROCESSABLE_ENTITY]
    }), STATUS_UNPROCESSABLE_ENTITY


@app.errorhandler(STATUS_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """
    Error handler for internal server error with status code 500.

    :param error:
    :return:
    """
    return jsonify({
        'success': False,
        'error': STATUS_INTERNAL_SERVER_ERROR,
        'message': STATUS_CODE_MESSAGES[STATUS_INTERNAL_SERVER_ERROR]
    }), STATUS_INTERNAL_SERVER_ERROR
