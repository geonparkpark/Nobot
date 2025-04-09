# Python 3.11 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 생성
WORKDIR /app

# 시스템 패키지 설치 (ffmpeg 포함)
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 코드 복사
COPY . .

RUN chmod +x /entrypoint.sh

CMD ["./entrypoint.sh"]
