# Python 3.11 기반 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
       curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENTRYPOINT을 쉘 스크립트로 대체
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["./entrypoint.sh"]

