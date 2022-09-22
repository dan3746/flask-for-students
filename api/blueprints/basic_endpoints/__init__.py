# from flask import Blueprint, request
#
# blueprint = Blueprint('api', __name__, url_prefix='/basic_api')
#
#
# @blueprint.route('/')
# def index():
#     return {'message': 'Hello World page'}
#
#
# @blueprint.route('/about')
# def about():
#     return {'message': 'About page'}
#
#
# @blueprint.route('/records')
# def records():
#     return {'message': 'Page with statistics'}
#
#
# @blueprint.route('/add_record', methods=['POST'])
# def add_record():
#     if request.method == "POST":
#         return {
#             'message': 'This endpoint should create a statics about the game',
#             'method': request.method,
#             'body': request.json
#         }
#
#
# @blueprint.route('/user/<int:id>')
# def user():
#     return {'message': 'Page with user info'}
