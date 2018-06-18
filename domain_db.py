import datetime
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker

__author__ = 'gru'


from onion_domain import OnionDomain


class OnionDbHandler:

    def __init__(self, db):
        self.db = db
        # Create an engine that stores data in the local directory's
        # sqlalchemy_example.db file.
        self.engine = create_engine('sqlite:///' + self.db)

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