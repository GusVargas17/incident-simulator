from incident.models import Incident
from collections import deque
from datetime import datetime

# Internal ID counter to generate unique incidents IDs
incident_id_counter = 1

# Queue to hold incidents that are pending
_pending_incidents = deque()

# List of track resolved incidents (history)
_resolved_incidents = []

def register_incident(type: str, priority: str, description: str) -> Incident:
    """
    Registers a new incident and adds it to the pending queue.
    Incidents with high priority are placed at the front of the queue.
    """

    global incident_id_counter

    #Validate priority level
    if priority.lower() not in ["low", "medium", "high"]:
        raise ValueError("Priority not accepted")

    # Created a new incident object
    incident = Incident(
        id=incident_id_counter,
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

    # Increment ID counter for the next incident
    incident_id_counter += 1

    return incident

def get_pending_incident() -> list[Incident]:
    """
    Returns a list of all pending incidents in the queue.
    """
    return list(_pending_incidents)

def assign_incident(incident_id: int, estimated_minutes: int = 30) -> Incident:
    """
    Assign an incident by its ID using business rules.
    Raises ValueError if assignment fails.
    """
    incident = next((i for i in _pending_incidents if i.id == incident_id), None)
    if not incident:
        raise ValueError("Incident not found")

    if incident.assigned_to is not None or incident.status != "pending":
        pass

def resolve_incident(incident_id: int, operator_name: str) -> Incident:
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

            # Update status and move to resolved history
            incident.status = "resolved"
            _pending_incidents.remove(incident)
            _resolved_incidents.append(incident)
            return incident

    # If no incident matched the ID
    raise ValueError("Incident not found")