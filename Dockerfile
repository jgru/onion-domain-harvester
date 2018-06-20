FROM python:3
MAINTAINER gru

RUN apt-get update && apt-get install -y tor

WORKDIR /usr/src/app
#VOLUME ["/usr/src/app/data"]

RUN git clone https://github.com/jgru/onion-domain-harvester.git
RUN pip install --no-cache-dir -r ./onion-domain-harvester/requirements.txt

#RUN mv ./onion-domain-harvester/crontab /etc/cron.d/cronjob
COPY ./crontab /etc/cron.d/cronjob
COPY ./test.py ./onion-domain-harvester/test.py
COPY ./main_harvester.py /usr/src/app/onion-domain-harvester/main_harvester.py
RUN crontab /etc/cron.d/cronjob


CMD cron -f

#CMD python ./onion-domain-harvester/main_harvester.py
