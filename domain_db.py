__author__ = 'gru'

import sqlite3
from onion_domain import OnionDomain

class DomainDbHandler:
    # Here will be the instance stored.
    __instance = None
    DB_PATH = "./example.db"

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DomainDbHandler.__instance is None:
            DomainDbHandler()
        return DomainDbHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DomainDbHandler.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DomainDbHandler.__instance = self
            self.conn = None

    def update(self, onion_domains):
        if self.conn is None:
            self.conn = sqlite3.connect(DomainDbHandler.DB_PATH)

        c = self.conn.cursor()
        self.conn.commit()
        self.conn.close()

