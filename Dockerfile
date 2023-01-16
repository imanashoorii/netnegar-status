FROM python:3.9.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y build-essential gcc \
  && apt-get install -y default-libmysqlclient-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings", "healthStatus.settings"]
EXPOSE 8000
