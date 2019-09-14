FROM library/python:3.7.1-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh && \
    apk add build-base

RUN apk add bash
RUN apk add pcre-dev 
RUN pip install --upgrade pip

RUN pip install -r requirements.txt 
RUN pip install git+https://github.com/LIAAD/py-pampo.git
RUN pip install gunicorn

ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp


EXPOSE 8000			
CMD gunicorn --bind 0.0.0.0:8000 wsgi 
