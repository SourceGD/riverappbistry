FROM python:3.10.14
WORKDIR .
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg
RUN apt install libgl1-mesa-glx libsm6 libxext6 nano -y
RUN pip install --upgrade pip
RUN pip install flask


COPY src/api /srv/riverapp/api
COPY src /srv/riverapp/api/src
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
ENV FLASK_APP=app
CMD ["nohup", "python", "app.py", "&"]

CMD ["tail", "-f", "/dev/null"]
