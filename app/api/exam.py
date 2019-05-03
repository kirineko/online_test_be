import time

from flask import request
from sqlalchemy import and_

from . import api
from .utils import jsonerr, jsonsucc
from ..models import Exam, Answer


@api.route('/exam')
def exam():
    args = request.values
    openid = args.get('openid')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    q = Exam.query.filter(and_(Exam.start_time <= current_time, Exam.end_time >= current_time)).all()
    if not q:
        return jsonerr(-1, '当前时间还没有可以参加的考试~')
    exams_ing = _get_exam(q)

    q = Answer.query.filter_by(openid=openid).all()
    exams_user = [{'gid': i.gid, 'score': i.total, 'submit_time': str(i.submit_time)} for i in q]
    exams_gid = [ex.get('gid') for ex in exams_user]
    q = Exam.query.filter(Exam.gid.in_(exams_gid)).all()
    exams_ed = _get_examed(q, exams_user)
    exams_ing = [exam for exam in exams_ing if exam['gid'] not in exams_gid]

    result = {
        'exams_ing': exams_ing,
        'exams_ed': exams_ed
    }
    return jsonsucc(result)


def _get_exam(exam_objects):
    exams = []
    for exam in exam_objects:
        exams.append({
            'gid': exam.gid,
            'gname': exam.gname,
            'lname': exam.lname,
            'start_time': str(exam.start_time),
            'end_time': str(exam.end_time),
            'total': exam.total
        })
    return exams


def _get_examed(exam_objects, exam_user):
    exams = []
    for eu in exam_user:
        for exam in exam_objects:
            if eu['gid'] == exam.gid:
                eu['gname'] = exam.gname
                eu['lname'] = exam.lname
                eu['start_time'] = str(exam.start_time)
                eu['end_time'] = str(exam.end_time)
                eu['total'] = exam.total
                exams.append(eu)
    return exams
