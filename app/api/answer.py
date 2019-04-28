import json
import time
from flask import request
from . import api
from .utils import jsonsucc
from .. import db
from ..models import Question, Answer


@api.route('/postanswer', methods=['post'])
def postanswer():
    args = request.get_json()
    gid = args.get('gid')
    submit_answers = args.get('answers')

    question_list = Question.query.filter_by(gid=gid).all()
    std_answers = [{'num': q.num, 'answer': q.answer, 'score': q.score} for q in question_list]
    score_result = _getscore(submit_answers, std_answers)

    answer_to_db = {
        'gid': gid,
        'gname': args.get('gname'),
        'answers': json.dumps(submit_answers),
        'openid': args.get('openid'),
        'total': score_result['total'],
        'submit_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    answer = Answer(**answer_to_db)
    db.session.add(answer)
    db.session.commit()

    return jsonsucc(answer_to_db)


def _getscore(submit_answers, std_answers):
    results = {}
    wrong_answers = []
    total = 0

    for std_answer in std_answers:
        num = std_answer['num']
        answer = std_answer['answer']
        score = std_answer['score']
        for s_num, s_answer in submit_answers.items():
            if num == int(s_num):
                score_got = score if answer == s_answer else 0
                if answer != s_answer:
                    wrong_answers.append(num)
                results[num] = {
                    'score': score_got,
                    'answer': answer
                }
                total += score_got

    results['wrong_answers'] = wrong_answers
    results['total'] = total
    return results
