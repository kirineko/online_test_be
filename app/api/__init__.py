from flask import Blueprint

api = Blueprint('api', __name__)

from . import errors, login, question, answer, exam, userauth
