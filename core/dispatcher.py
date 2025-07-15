from incident.models import Incident
from collections import deque
from datetime import datetime

incident_id_counter = 1
_pending_incidents = deque()
_available_operators = {"Sofia", "Carlos", "Mariano"}

def register_incident(type: str, priority: str, description: str) -> Incident:
    global incident_id_counter

    if priority.lower() not in ["low", "medium", "high"]:
        raise ValueError("Priority not accepted")

    incident = Incident(
        id=incident_id_counter,
        type=type,
        priority=priority.lower(),
        description=description,
        created_at=datetime.now(),
        assigned_to=None,
        status="pending"
    )

    if priority.lower() == "high":
        _pending_incidents.appendleft(incident)
    else:
        _pending_incidents.append(incident)

    incident_id_counter += 1

    return incident

def get_pending_incident() -> list[Incident]:
    return list(_pending_incidents)

def assign_incident(incident_id: int, operator_name: str) -> Incident:
    if operator_name not in _available_operators:
        raise ValueError("Operator not found")

    for incident in _pending_incidents:
        if incident.id == incident_id:
            if incident.assigned_to is not None:
                raise ValueError("Incident is already assigned")
            if incident.status != "pending":
                raise ValueError("Incident is not in a pending state")
            
            # all good: assign operator and change state
            incident.assigned_to = operator_name
            incident.status = "in_progress"
            return incident

    # if the for ends without finding it
    raise ValueError("Incident not found")