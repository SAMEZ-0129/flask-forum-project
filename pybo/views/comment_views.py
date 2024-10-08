# from datetime import datetime

# from flask import Blueprint, render_template, request, url_for, g, flash
# from werkzeug.utils import redirect

# from .. import db
# from ..models import Answer # from pybo.models import Question 이랑 동일한 코드임
# from ..forms import QuestionForm, AnswerForm
# from ..views.auth_views import login_required

# @bp.route('/create/answer/<int:answer_id>', methods=('GET', 'POST'))
# def create_answer(answer_id):
#     form = CommentForm()
#     answer = Answer.query.get_or_404(answer_id)
#     if request.method == 'POST' and form.validate_on_submit():
#         if(g.user):
#             comment = Comment(user=g.user, content=form.content.data, create_date=datetime.now(), answer=answer)
#         else:
#             comment = Comment(content=form.content.data, create_date=datetime.now(), answer=answer)
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('question.detail', question_id=answer.question.id))
#     return render_template('comment/comment_form.html', form=form)