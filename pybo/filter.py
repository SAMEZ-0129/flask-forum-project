def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'): # value로 전달받은 datetime객체를 날짜형식 포맷(fmt)로 변환해서 리턴해줌
    return value.strftime(fmt)