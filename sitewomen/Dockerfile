FROM python:3.12-slim

RUN groupadd -r groupdjnago && useradd -r -g groupdjnago userdj

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBITECODE=1

RUN pip install --upgrade pip
WORKDIR /app/www/sitewomen
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
USER userdj