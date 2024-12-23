from dviu_timetable.core.providers.impl.domain_provider import DomainProviderImpl
from dviu_timetable.core.providers.impl.meta_provider import MetaProviderImpl
from dviu_timetable.core.providers.impl.group_provider import GroupProviderImpl


domain_provider = DomainProviderImpl()

domains = domain_provider.get_domains()
domain = domains[0]

meta_provider = MetaProviderImpl(domain, domain_provider)
group_provider = GroupProviderImpl(domain, domain_provider, meta_provider)

print(group_provider.get_group_by_id(1111))
