FROM python:3.7
MAINTAINER Nikita Grishin <grishin.na@phystech.edu>

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./src /src
WORKDIR /src


CMD [ "python", "./case_consumer.py" ]