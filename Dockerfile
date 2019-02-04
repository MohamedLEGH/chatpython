FROM ubuntu:18.10
LABEL maintainer="Mohamed Amine LEGHERABA <mlegheraba@protonmail.com>"
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi flask flask-socketio eventlet
COPY ./ ./app
WORKDIR ./app
EXPOSE 5000
CMD [ "python3", "./server.py" ]

