FROM robcherry/docker-chromedriver:latest

RUN apt-get update && apt-get install -y libpq-dev
RUN apt-get install -y python3-dev
RUN apt-get install -y gcc python3-dev postgresql postgresql-contrib
RUN apt-get install -y python3-venv
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-wheel
RUN apt-get install gcc libpq-dev -y
RUN apt-get install python-dev  python-pip -y
RUN apt-get install python3-dev python3-pip python3-venv python3-wheel -y
RUN pip3 install wheel

COPY requirements.txt requirements.txt
#RUN python3 -m venv venv
#RUN venv/bin/pip3 install -r requirements.txt

RUN pip3 install -r requirements.txt

COPY app.py .
COPY boot.sh .
COPY config.py .
COPY download.py .
COPY models.py .
COPY service.py .
COPY timeout.py .

RUN chmod +x boot.sh

# start service
ENTRYPOINT ["./boot.sh"]
