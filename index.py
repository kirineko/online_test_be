import os
from app import create_app, db
from app.models import Answer, Question, Exam, CSessionInfo, User
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Answer=Answer,
        Question=Question,
        Exam=Exam,
        CSessionInfo=CSessionInfo,
        User=User
    )
