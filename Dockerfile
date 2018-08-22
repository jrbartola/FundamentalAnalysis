FROM python:3.6

RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends \
    netcat \
  && apt-get -q clean

ADD backend/ /backend
ADD start.sh /start.sh
WORKDIR /backend

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ../start.sh