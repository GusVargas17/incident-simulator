from incident.models import Incident
from core.operator import Operator
from core.operators import OPERATORS
from typing import Optional

def find_available_operator_for_incident(incident: Incident) -> Optional[Operator]:
    """
    Find an available operator for the given incident based on type and availability.  
    """
    for operator in OPERATORS.values():
        if (
            operator.is_avaliable()
            and (incident.type in operator.specialties or "all" in operator.specialties)
        ):
            return operator
    return None

def assign_incident_to_operator(incident: Incident, estimated_minutes: int = 30) -> bool:
    """
    Assign the incident to an appropriate operator.
    Returns True if assignment was successful, False otherwise.
    """
    operator = find_available_operator_for_incident(incident)
    if operator:
        operator.assign_incident(incident.id, estimated_minutes)
        incident.assigned_to = operator.name
        operator.status = "in_progress"
        return True
    return False