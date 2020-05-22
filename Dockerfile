FROM python:3.6

RUN apt-get update && apt-get install -y vim curl jq
RUN pip3 install requests graphyte python-dateutil
RUN mkdir /code
COPY run.py /code/run.py
COPY runner.sh /code/runner.sh
WORKDIR /code
CMD "./runner.sh"
