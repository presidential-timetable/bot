import json
import logging
from pathlib import Path

from dviu_timetable.core.models.domain import Domain
from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider

_logger = logging.getLogger(__name__)

class DomainProviderImpl(AbstractDomainProvider):
    def __init__(self):
        self._domains_list = json.loads(
            Path('data/domains.json').read_text(encoding='UTF-8')
        )
        _logger.debug(f'Built DomainProviderImpl with {len(self._domains_list)} domains.')

    def get_domains(self) -> list[Domain]:
        # _logger.debug(f'DomainProviderImpl.get_domains()')

        return [
            Domain.get_from_dict(domain_dict) for domain_dict in self._domains_list
        ]

    def get_domain_by_id(self, domain_id: int) -> Domain:
        # _logger.debug(f'DomainProviderImpl.get_domain_by_id({domain_id=})')

        for domain in self.get_domains():
            if domain.domain_id == domain_id:
                return domain

        raise Exception(f'domain {domain_id} not found')
