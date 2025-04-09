#!/bin/bash

export $(grep -v '^#' .env | xargs)

# Redis 이벤트 리스너 백그라운드 실행
python redis_update_url.py &

# FastAPI 앱 실행
exec uvicorn main:app --host 0.0.0.0 --port 8000
