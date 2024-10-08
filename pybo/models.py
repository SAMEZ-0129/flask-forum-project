from pybo import db

# 추천 기능을 위한 모델 (N:N 관계)
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)
answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id',db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

# Question 클래스를 통해 질문 모델 생성
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True) # 수정 일시
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set')) # 추천인



# Answer 클래스를 통해 답변 모델 생성
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True) # 수정 일시
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

# 회원가입을 위한 회원 모델
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


# 댓글(Comment) 기능 추가 모델
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
#     user = db.relationship('User',backref=db.backref('comment_set'))
#     content = db.Column(db.Text(), nullable=False)
#     create_date = db.Column(db.DateTime(), nullable=False)
#     modify_date = db.Column(db.DateTime())
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
#     question = db.relationship('Answer', backref=db.backref('comment_set'))
#     answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=False)
#     answer = db.relationship('Answer', backref=db.backref('comment_set'))