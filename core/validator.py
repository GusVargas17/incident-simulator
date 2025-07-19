from core.operators import OPERATORS

VALID_PRIORITY = {"low", "medium", "high"}
VALID_INCIDENT_TYPE = {"software", "hardware", "network", "security", "ux", "database"}

def is_valid_operator_name(name: str) -> bool:
    return name in OPERATORS

def is_valid_priority(priority: str) -> bool:
    """
    Check if the priority level is valid.
    """
    return priority.lower() in VALID_PRIORITY

def is_valid_incident_type(incident_type: str) -> bool:
    """
    Check if the incident type is valid.
    """
    return incident_type in VALID_INCIDENT_TYPE

def is_valid_status(status: str) -> bool:
    """
    Check if the incident status is valid.
    """
    return status in ["new", "assigned", "in_progress", "escalated", "resolved"]


def is_valid_incident_id_format(incident_id: str) -> bool:
    """
    Validates if the ID is a 3-digit numeric string (e.g., '001').
    """
    return incident_id.isdigit() and len(incident_id) == 3


def is_unique_incident_id(incident_id: str, existing_incidents: list) -> bool:
    """
    Checks if the incident ID is unique within a list of incidents.
    """
    all_ids = [i.id for i in existing_incidents]
    return incident_id not in all_ids