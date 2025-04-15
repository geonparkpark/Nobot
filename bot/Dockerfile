# Python 3.11 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 생성
WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# 봇 실행 명령
CMD ["python3", "bot.py"]