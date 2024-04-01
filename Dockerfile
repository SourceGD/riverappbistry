FROM python:3.10.14-alpine3.19
WORKDIR .
RUN pip install --upgrade pip
RUN pip install flask
ADD . /srv
WORKDIR /srv/riverapp/api
RUN pip install -r requirements.txt

ENV FLASK_APP=app

CMD ["python","app.py"]