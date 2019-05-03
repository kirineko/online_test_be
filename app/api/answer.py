import json
import time
from flask import request
from . import api
from .utils import jsonsucc, jsonerr
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


@api.route('/getanswer', methods=['get'])
def getanswer():
    args = request.values
    openid = args.get('openid')
    gid = args.get('gid')

    answer = Answer.query.filter_by(openid=openid).filter_by(gid=gid).first()
    if answer is None:
        return jsonerr(-1, '获取答案失败')
    submit_answers = json.loads(answer.answers)

    question_list = Question.query.filter_by(gid=gid).order_by(Question.num).all()
    std_answers = [{'num': q.num, 'answer': q.answer, 'score': q.score} for q in question_list]

    results = _getscore(submit_answers, std_answers)
    results['gname'] = answer.gname
    print(answer.submit_time)
    results['submit_time'] = str(answer.submit_time)
    return jsonsucc(results)


@api.route('/getuseranswer', methods=['get'])
def getuseranswer():
    args = request.values
    openid = args.get('openid')
    gid = args.get('gid')

    answer = Answer.query.filter_by(openid=openid).filter_by(gid=gid).first()
    if answer is None:
        return jsonsucc('')
    return jsonsucc(json.loads(answer.answers))


def _getscore(submit_answers, std_answers):
    results = {}
    total = 0
    data = []

    for std_answer in std_answers:
        num = std_answer['num']
        answer = std_answer['answer']
        score = std_answer['score']
        for s_num, s_answer in submit_answers.items():
            if num == int(s_num):
                score_got = score if answer == s_answer else 0

                data.append({
                    'num': num,
                    'user_answer': s_answer,
                    'std_answer': answer,
                    'right': answer == s_answer
                })
                total += score_got

    results['data'] = data
    results['total'] = total
    return results
