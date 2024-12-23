from __future__ import annotations

from dataclasses import dataclass

@dataclass
class Domain:
    domain_id: int
    domain_name: str

    @classmethod
    def get_from_dict(cls, domain_dict: dict) -> Domain:
        return Domain(
            domain_id=domain_dict['domain_id'],
            domain_name=domain_dict['domain_name']
        )
