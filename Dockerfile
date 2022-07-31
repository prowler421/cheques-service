FROM python:3.10.5-bullseye

WORKDIR /cheques-service
COPY ./pyproject.toml .
COPY ./poetry.lock .
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY . .

RUN apt-get update
RUN apt-get install -y wget gnupg2 software-properties-common

RUN wget -qO - http://packages.confluent.io/deb/7.2/archive.key | apt-key add -
RUN add-apt-repository "deb [arch=amd64] http://packages.confluent.io/deb/7.2 stable main"
RUN apt-get update
RUN apt-get install -y librdkafka1
RUN apt-get install -y librdkafka-dev

#RUN apt update
#RUN apt-get install librdkafka1
#RUN apt-get install librdkafka++1
#RUN apt-get install librdkafka++1-dbgsym
#RUN apt-get install librdkafka-dev
#RUN apt-get install librdkafka1-dbgsym

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
EXPOSE 8000