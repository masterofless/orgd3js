FROM ubuntu:latest

MAINTAINER Andy Cohan "andy@cohan.org"

RUN apt-get update -y && \
    apt-get install -y python3-pip

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python3", "app.py" ]
EXPOSE 8080
