__author__ = 'gru'

import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, ForeignKey, Integer, String, Date

from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


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


class OnionDbHandler:

    def __init__(self, db_path):
        self.db_path = db_path
        # Create an engine that stores data in the local directory's
        # sqlalchemy_example.db file.
        self.engine = create_engine('sqlite:///' + self.db_path)

        # Create all tables in the engine. This is equivalent to "Create Table"
        # statements in raw SQL.
        if not self.engine.dialect.has_table(self.engine,
                                             OnionDomain.__tablename__):  # If table
            # don't exist, Create.
            OnionDomain.metadata.create_all(self.engine)



        # A DBSession() instance establishes all conv   ersations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object.
        DBSession = sessionmaker(bind=self.engine)

        # Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.session = DBSession()

    def update_db(self, onion_domains):
        for d in onion_domains:
            is_existing = self.session.query(exists().where(
                OnionDomain.url == d.url)).scalar()

            if is_existing:
                today = datetime.date.today()
                self.session.query(OnionDomain).filter(OnionDomain.url == d.url).update({OnionDomain.last_seen: today})
                self.session.commit()
            else:
                # Insert new domain in table
                self.session.add(d)
                self.session.commit()

    def retrieve_domains(self):
        domains = self.session.query(OnionDomain).all()
        return domains


