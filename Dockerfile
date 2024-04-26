FROM python:3.10.14
WORKDIR .
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg
RUN apt install libgl1-mesa-glx libsm6 libxext6 nano -y
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install flask


COPY src/api /srv/riverapp/api
COPY src /srv/riverapp/api/src
COPY src/api/flaskapp.conf /etc/apache2/sites-available/
COPY src/api/wsgi.py /srv/riverapp/api
COPY libs/pyorc /srv/riverapp/api/libs/pyorc
COPY requirements.txt /srv/riverapp/
COPY src/api/.env /srv/riverapp/api
COPY definitions.py /srv/riverapp/api
WORKDIR /srv/riverapp
RUN pip install -r requirements.txt
RUN pip install python-dotenv
RUN pip install opencv-python
RUN pip install waitress
WORKDIR /srv/riverapp/api
RUN a2ensite flaskapp && a2enmod wsgi
EXPOSE 80
ENV FLASK_APP=app

CMD ["tail", "-f", "/dev/null"]
