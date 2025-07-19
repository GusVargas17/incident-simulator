from incident.models import Incident
from typing import List

def filter_by_status(incidents: List[Incident], status: str) -> List[Incident]:
    return [i for i in incidents if i.status == status]

def filter_by_priority(incidents: List[Incident], priority: str) -> List[Incident]:
    return [i for i in incidents if i.priority == priority]

def filter_unassigned(incidents: List[Incident]) -> List[Incident]:
    return [i for i in incidents if i.assigned_to is None]

def filter_by_operator(incidents: List[Incident], operator_name: str) -> List[Incident]:
    return [i for i in incidents if i.assigned_to == operator_name]