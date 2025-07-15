from incident.models import Incident
from collections import deque
from datetime import datetime

incident_id_counter = 1
_pending_incidents = deque()

def register_incident(type: str, priority: str, description: str) -> Incident:
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

    global incident_id_counter
    incident_id_counter += 1

    return incident

def get_pending_incident() -> list[Incident]:
    return list(_pending_incidents)