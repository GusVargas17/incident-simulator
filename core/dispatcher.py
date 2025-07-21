from incident.models import Incident
from rules.assignment_rules import assign_incident_to_operator
from rules.validation import can_operator_resolve_incident, is_valid_role_to_resolve
from core.operators import OPERATORS
from core.validator import is_valid_priority
from core.id_generator import generate_incident_id
from persistence.storage import (
    save_escalated_incident, load_escalated_incident,
    save_resolved_incident, load_resolved_incident
)
from collections import deque
from datetime import datetime

# Queue to hold incidents that are pending
_pending_incidents = deque()

# List of track resolved incidents (history)
_resolved_incidents = load_resolved_incident()

# List of track escalated incidents
_escalated_incidents = load_escalated_incident()
# -------------------- #
# DISPATCHER FUNCTIONS #
# -------------------- #

def register_incident(type: str, priority: str, description: str) -> Incident:
    """
    Registers a new incident and adds it to the pending queue.
    Incidents with high priority are placed at the front of the queue.
    """

    #Validate priority level
    if not is_valid_priority(priority):
        raise ValueError("Priority not accepted")

    # Created a new incident object
    incident = Incident(
        id=generate_incident_id(),
        type=type,
        priority=priority.lower(),
        description=description,
        created_at=datetime.now(),
        assigned_to=None,
        status="pending"
    )

    # Add to front if high priority, otherwise add to the back
    if priority.lower() == "high":
        _pending_incidents.appendleft(incident)
    else:
        _pending_incidents.append(incident)

    return incident

def get_pending_incident() -> list[Incident]:
    """
    Returns a list of all pending incidents in the queue.
    """
    return list(_pending_incidents)

def assign_incident(incident_id: str, estimated_minutes: int = 30) -> Incident:
    """
    Assign an incident by its ID using business rules.
    Raises ValueError if assignment fails.
    """
    incident = next((i for i in _pending_incidents if i.id == incident_id), None)
    if not incident:
        raise ValueError("Incident not found")

    if incident.assigned_to is not None or incident.status != "pending":
        raise ValueError("Incident is not available for assignment")

    success = assign_incident_to_operator(incident, estimated_minutes)
    if not success:
        raise ValueError("No available operator could handle this incident")

    return incident

def start_incident(incident_id: str, operator_name: str) -> Incident:
    """
    Moves an incident to 'in_progress' status if assigned and valid.
    """
    for incident in _pending_incidents:
        if incident.id == incident_id:
            if incident.assigned_to != operator_name:
                raise ValueError("Incident not assigned to this operator")
            if incident.status != "pending":
                raise ValueError("Only pending incidents can be started")

            incident.status = "in_progress"
            return incident

    raise ValueError("Incident not found")

def resolve_incident(incident_id: str, operator_name: str) -> Incident:
    """
    Resolves an assigned incident, if it is in progress and handled by the right operator.
    """
    for incident in _pending_incidents:
        if incident.id == incident_id:

            # Validation: must be assigned before resolving
            if incident.assigned_to is None:
                raise ValueError("Incident is not assigned")
            # Validation: only the assigned operator can resolve it
            if incident.assigned_to != operator_name:
                raise ValueError("Different Operator")
            # Validation: only incidents in progress can be resolved
            if incident.status != "in_progress":
                raise ValueError("Incident cannot be resolved in its current state")
            # Validation: operator must have permission to resolve this type
            if not can_operator_resolve_incident(operator_name, incident):
                raise ValueError("Operator lacks permission to resolve this incident type")
            # Validate role
            operator = OPERATORS.get(operator_name)
            if not is_valid_role_to_resolve(operator.role, incident.type):
                raise ValueError("Operator role is not allowed to resolve this type")

            # Update status and move to resolved history
            incident.status = "resolved"
            _pending_incidents.remove(incident)
            _resolved_incidents.append(incident)
            return incident

    # If no incident matched the ID
    raise ValueError("Incident not found")

def escalate_incident(incident_id: str, reason: str) -> Incident:
    """
    Escalates an incident that could not be resolved.
    """
    for incident in _pending_incidents:
        if incident.id == incident_id:
            incident.status = "escalated"
            _pending_incidents.remove(incident)
            _escalated_incidents.append(incident)
            save_escalated_incident(incident)
            return incident

    # If no incident matched the ID
    raise ValueError("Incident not found")

def get_resolved_incidents() -> list[Incident]:
    """
    Returns all resolved incidents.
    """
    return _resolved_incidents


def get_escalated_incidents() -> list[Incident]:
    """
    Returns all escalated incidents.
    """
    return _escalated_incidents