from datetime import datetime
from core.dispatcher import _pending_incidents
from incident.models import Incident
from rules.escalation_rules import should_escalate_incident, escalate_incident

#List of escalated incidents
_escalated_incidents = []

def get_time_limit(priority: str) -> int:
    """
    Returns the maximum allowed time (in minutes) of an incident
    can remain unassigned based on its priority level.
    
    Accepted priorities: "high", "medium", "low"
    """

    # Normalize the priority to lowercase
    priority = priority.lower()

    # Dictionary of priority to maximum waiting time in minutes
    priority_limits = {
        "high": 2,
        "medium": 5,
        "low": 7
    }

    if priority not in priority_limits:
        raise ValueError(f"Unknown priority: {priority}")

    return priority_limits[priority]

def escaled_if_needed(priority: str):
    """
    Escalates unassigned incidents that exceeded their allowed waiting time.
    Moves them from _pending_incidents to _escalated_incidents.
    """

    to_escalate = []

    for incident in _pending_incidents:
        # Only escalate unassigned incidents
        if incident.assigned_to is not None:
            continue

        try:
            limit = get_time_limit(incident.priority)
        except ValueError:
            continue   # Skip unknown priorities

        if should_escalate_incident(incident, limit):
            escalate_incident(incident)
            incident.status = "escalated"
            to_escalate.append(incident)

    # Remove escalated incidents from the pending queue and store them
    for i in to_escalate:
        _pending_incidents.remove(i)
        _escalated_incidents.append(i)