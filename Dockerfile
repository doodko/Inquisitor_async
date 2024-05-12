FROM python:3.12-slim

ENV PYTHONPATH=/app/ \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=0 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

COPY requirements/base.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD ["python", "start_bot.py"]