import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) # DB 접속 URL
SQLALCHEMY_TRACK_MODIFICATIONS = False # SQLAlchemy 이벤트 처리 옵션 > 필요없어서 비활성화

# 1. flask db migrate = 모델을 새로 생성하거나 변경할 때 사용
# 2. flask db upgrade = 모델의 변경 내용을 실제 DB에 적용할 때 사용

SECRET_KEY = 'dev' # 실 운영 시 복잡한 값으로 세팅 필수