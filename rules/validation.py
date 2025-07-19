from core.operators import OPERATORS
from incident.models import Incident

def can_operator_resolve_incident(operator_name: str, incident: Incident) -> bool:
    """
    Check if a given operator has permission to resolve the given incident.
    """
    operator = OPERATORS.get(operator_name)
    if not operator:
        return False
    if "all" in operator.specialties:
        return True

    return incident.type in operator.specialties

def is_valid_role_to_resolve(role: str, incident_type: str) -> bool:
    """
    Define rol-based permissions for resolving certain incident types.
    """
    permissions = {
        "support_level_1": ["software", "ux", "network"],
        "support_level_2": ["hardware", "software", "security", "network", "database"],
        "admin": ["all"]
    }

    allowed = permissions.get(role, [])
    return incident_type in allowed or "all" in allowed