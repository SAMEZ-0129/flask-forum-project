from datetime import datetime
from sqlalchemy import func

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db
from ..models import Question, Answer, User, question_voter # from pybo.models import Question 이랑 동일한 코드임
from ..forms import QuestionForm, AnswerForm
from ..views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

# 검색 기능 추가
@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')
    # 정렬 파트
    if so == 'recommend':
        sub_query = db.session.query(
            question_voter.c.question_id, func.count('*').label('num_voter'))\
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query.outerjoin(sub_query, Question.id == sub_query.c.question_id)\
        .order_by(sub_query.c.num_voter_desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(
            Answer.question_id, func.count('*').label('num_answer'))\
            .group_by(Answer.question_id).sub_query()
        question_list = Question.query.outerjoin(sub_query, Question.id == sub_query.c.question_id)\
        .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회 파트
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=20)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

# 질문 폼 저장하기
@bp.route('/create/', methods =('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit(): # form.validate_on_submit을 통해 전송된 폼 데이터의 정합성 검사
        question = Question(subject=form.subject.data, content = form.content.data, create_date = datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)


# 질문 수정
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj = question)
    return render_template('question/question_form.html', form=form)


# 질문 삭제
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

# 질문 추천 
@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할 수 없습니다.')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

