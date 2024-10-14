from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

import config

# SQLite DB의 ORM 사용 시 발생하는 문제점 해결을 위한 코드
naming_convetion = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention = naming_convetion))
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    app.config.from_object(config) # app 환경변수로 부르기 위해 지정(config.py)

    # ORM (object relational mapping)
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    migrate.init_app(app, db)
    from . import models

    # BluePrint
    from .views import main_view, question_views, answer_views, auth_views
    app.register_blueprint(main_view.bp)    # main_view.py에서 생성한 블루프린트 객체(bp) 적용
    app.register_blueprint(question_views.bp)   # 질문 목록 블루프린트에 등록
    app.register_blueprint(answer_views.bp)     # 답변 목록 블루프린트에 등록
    app.register_blueprint(auth_views.bp)       # 회원가입 블루프린트 등록

    # datetime Filter
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown
    Markdown(app, extension=['n12br', 'fenced_code'])

    # 오류페이지
    app.register_error_handler(404, page_not_found)

    return app