FROM python:3.12-slim

WORKDIR /app

COPY url_updater/ .
COPY shared/ .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "redis_update_url.py"]