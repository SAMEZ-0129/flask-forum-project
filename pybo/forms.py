# 질문을 등록할 때 사용할 모듈
from flask_wtf import FlaskForm 

# 글자수 제한이 있는 제목은 StringField, 제한 없는 내용은 TextAreaField
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# 질문 작성
class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목을 입력해 주세요.')])
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력해 주세요.')])

# 답변 작성
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('답변 내용을 작성해주세요.')])

# 회원가입
class UserCreateForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 2차 확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

# 로그인
class UserLoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])