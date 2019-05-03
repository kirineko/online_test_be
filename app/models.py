from . import db


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.INTEGER, primary_key=True)
    openid = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    gid = db.Column(db.INTEGER, nullable=False)
    gname = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    answers = db.Column(db.String(300, 'utf8mb4_unicode_ci'), nullable=False)
    total = db.Column(db.INTEGER, nullable=False)
    submit_time = db.Column(db.DATETIME, nullable=False)


class CSessionInfo(db.Model):
    __tablename__ = 'cSessionInfo'

    open_id = db.Column(db.String(100, 'utf8mb4_unicode_ci'), primary_key=True)
    uuid = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    skey = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    create_time = db.Column(db.DATETIME, nullable=False)
    last_visit_time = db.Column(db.DATETIME, nullable=False)
    session_key = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    user_info = db.Column(db.String(2048, 'utf8mb4_unicode_ci'), nullable=False)


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.INTEGER, primary_key=True)
    gid = db.Column(db.INTEGER, nullable=False)
    gname = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    num = db.Column(db.INTEGER, nullable=False, index=True)
    type = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    content = db.Column(db.String(200, 'utf8mb4_unicode_ci'), nullable=False)
    answer = db.Column(db.String(30, 'utf8mb4_unicode_ci'), nullable=False)
    score = db.Column(db.INTEGER, nullable=False)
    result_a = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    result_b = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    result_c = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    result_d = db.Column(db.String(50, 'utf8mb4_unicode_ci'))


class Exam(db.Model):
    __tablename__ = 'exam'

    id = db.Column(db.INTEGER, primary_key=True)
    gid = db.Column(db.INTEGER, nullable=False, unique=True, index=True)
    gname = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    lname = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    total = db.Column(db.INTEGER, default=100)
    start_time = db.Column(db.DATETIME, nullable=False)
    end_time = db.Column(db.DATETIME, nullable=False)
