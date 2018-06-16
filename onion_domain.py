__author__ = 'gru'

import datetime

from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OnionDomain(Base):
    __tablename__ = 'onion_domain'

    url = Column(String(250), primary_key=True, nullable=False)
    title = Column(String(250), nullable=False)
    description = Column(String(1500), nullable=True)
    first_seen = Column(Date, default=datetime.date.today())
    last_seen = Column(Date, default=datetime.date.today())

    def __init__(self, url, title, desc, now):

        self.url = url
        self.title = title.strip()
        self.description = desc
        self.first_seen =now
        self.last_seen = now

    def __hash__(self):
        return hash(self.url)

    def __str__(self):
        return("URL: " + self.url + "\nTitle: " + self.title
               + "\nDescription: " +
               self.description)

    def get_url(self):
        return self.url

    def get_description(self):
        return self.description

    def __eq__(self, other):
        return self.url == other.url


