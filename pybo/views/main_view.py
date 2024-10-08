from flask import Blueprint, url_for
from werkzeug.utils import redirect

from pybo.models import Question

 # 블루프린트 객체 생성
bp = Blueprint('main', __name__, url_prefix='/') # url_prefix를 통해 애너테이션(@app.rout같은) URL 앞에 기본으로 들어갈 접두어 URL 경로 설정

# route 함수 등록 -> 새로운 페이지 등록(creat app 함수에 추가할 필요 없이 새로운 페이지는 이 파일에 추가하여 init 파일이 가벼워짐)
@bp.route('/hello')
def hello_pybo():
    return 'Hello pybo~!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))