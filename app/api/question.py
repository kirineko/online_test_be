from flask import request
from . import api
from .utils import jsonerr, jsonsucc
from ..models import Question


@api.route('/question')
def question():
    args = request.values
    num = args.get('num', 1)
    q = Question.query.filter_by(num=num).first()
    if q is None:
        return jsonerr(-1, '没有题目啦~')
    dict_q = q.__dict__
    del dict_q['_sa_instance_state']
    del dict_q['answer']
    return jsonsucc(dict_q)
