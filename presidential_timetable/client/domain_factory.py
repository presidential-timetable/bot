from presidential_timetable.core.domain import Domain


class DomainFactory:
    def __init__(self):
        self.domains = {
            1: Domain(domain_id=1, domain_name='ДВИУ РАНХиГС: вышка'),
            2: Domain(domain_id=2, domain_name='ДВИУ РАНХиГС: СПО')
        }

    async def get_domains(self) -> list[Domain]:
        return list(self.domains.values())

    async def get_domain_by_id(self, domain_id: int) -> Domain:
        return self.domains.get(domain_id, None)
