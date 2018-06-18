FROM python:3
MAINTAINER gru

RUN apt-get update && apt-get install -y tor net-tools

WORKDIR /usr/src/app
VOLUME ["/usr/src/app/data"]

RUN git clone https://github.com/jgru/onion-domain-harvester.git
RUN pip install --no-cache-dir -r ./onion-domain-harvester/requirements.txt

CMD python ./onion-domain-harvester/main_harvester.py -d ./data/onion_domains.db
