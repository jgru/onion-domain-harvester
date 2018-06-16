from abc import ABC, abstractmethod


class AbstractOnionDomainParser(ABC):
    @property
    def targets(self):
        raise NotImplementedError

    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def parse_domain_list(self):
        pass

    @abstractmethod
    def print_harvested_domains(self):
        pass
