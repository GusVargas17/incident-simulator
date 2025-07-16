from datetime import datetime
from core.dispatcher import _pending_incidents, _escalated_incidents
from incident.models import Incident

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
        "medim": 5,
        "low": 7
    }

    if priority not in priority_limits:
        raise ValueError

    return priority_limits[priority]

def escaled_if_needed(priority: str):
    """
    Increases unassigned incidents if they have exceeded your time limit
    depending on your priority. Intensified incidents are removed from the tracks
    queue and added to a separate scaled list.
    """

    # We will temporarily store escalated incidents for secure disposal later.
    to_escalate = []

    for incident in _pending_incidents:
        # Only escalate unassigned incidents
        if incident.assigned_to is not None:
            continue

        # Get time limit in minutes for this incident's priority
        time_limit = get_time_limit(incident.priority)

        #Calculate how many minutes have passed since the incident was created
        minutes_passed = (datetime.now()) - incident.created_at.total_seconds() / 60

        # If time exceeded -> escalate
        if minutes_passed > time_limit:
            incident.status = "escalated"
            to_escalate.append(incident)

    # Remove escalated incidents from the pending queue and store them
    for i in to_escalate:
        _pending_incidents.remove(i)
        _escalated_incidents.append(i)