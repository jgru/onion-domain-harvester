FROM python:3
MAINTAINER gru

RUN apt-get update && apt-get install -y tor net-tools

WORKDIR /usr/src/app
VOLUME ["/usr/src/app/data"]

RUN git clone https://github.com/jgru/onion-domain-harvester.git
RUN pip install --no-cache-dir -r ./onion-domain-harvester/requirements.txt

RUN mv ./onion-domain-harvester/crontab /etc/cron.d/crontab
#RUN crontab /etc/cron.d/crontab

CMD cron -f
