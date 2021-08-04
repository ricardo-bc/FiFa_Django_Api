FROM python:3.7

EXPOSE 8200


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY . .