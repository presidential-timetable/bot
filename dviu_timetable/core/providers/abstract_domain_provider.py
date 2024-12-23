from abc import ABC, abstractmethod
from dviu_timetable.core.models.domain import Domain


class AbstractDomainProvider(ABC):
    @abstractmethod
    def get_domains(self) -> list[Domain]:
        raise NotImplementedError

    @abstractmethod
    def get_domain_by_id(self, domain_id) -> Domain:
        raise NotImplementedError
