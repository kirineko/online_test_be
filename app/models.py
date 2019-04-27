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


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.INTEGER, primary_key=True)
    isbn = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    openid = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    title = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    image = db.Column(db.String(100, 'utf8mb4_unicode_ci'))
    alt = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    publisher = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    summary = db.Column(db.String(1500, 'utf8mb4_unicode_ci'), nullable=False)
    price = db.Column(db.String(100, 'utf8mb4_unicode_ci'))
    rate = db.Column(db.Float(asdecimal=True))
    tags = db.Column(db.String(100, 'utf8mb4_unicode_ci'))
    author = db.Column(db.String(100, 'utf8mb4_unicode_ci'))
    count = db.Column(db.INTEGER, nullable=False)


class CSessionInfo(db.Model):
    __tablename__ = 'cSessionInfo'

    open_id = db.Column(db.String(100, 'utf8mb4_unicode_ci'), primary_key=True)
    uuid = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    skey = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    create_time = db.Column(db.DATETIME, nullable=False)
    last_visit_time = db.Column(db.DATETIME, nullable=False)
    session_key = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    user_info = db.Column(db.String(2048, 'utf8mb4_unicode_ci'), nullable=False)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.INTEGER, primary_key=True)
    openid = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    bookid = db.Column(db.String(10, 'utf8mb4_unicode_ci'), nullable=False)
    comment = db.Column(db.String(200, 'utf8mb4_unicode_ci'), nullable=False)
    phone = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    location = db.Column(db.String(50, 'utf8mb4_unicode_ci'))


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.INTEGER, primary_key=True)
    gid = db.Column(db.INTEGER, nullable=False)
    gname = db.Column(db.String(50, 'utf8mb4_unicode_ci'), nullable=False)
    num = db.Column(db.INTEGER, nullable=False, unique=True)
    type = db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable=False)
    content = db.Column(db.String(200, 'utf8mb4_unicode_ci'), nullable=False)
    answer = db.Column(db.String(30, 'utf8mb4_unicode_ci'), nullable=False)
    score = db.Column(db.INTEGER, nullable=False)
    result_a = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    result_b = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    result_c = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
    result_d = db.Column(db.String(50, 'utf8mb4_unicode_ci'))
