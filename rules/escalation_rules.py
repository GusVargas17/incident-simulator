from datetime import datetime, timedelta
from incident.models import Incident

def should_escalate_incident(incident: Incident, minutes_threshold: int = 30) -> bool:
    """
    Determinate if an incidente should be escalated based on time since creation.
    """
    elapsed = datetime.now() - incident.created_at
    return elapsed >= timedelta(minutes=minutes_threshold)

def escalate_incident(incident: Incident) -> None:
    """
    Escalate incident priority and mark it as requiring urgent attention.
    """
    if incident.priority == "low":
        incident.priority = "medium"
    if incident.priority == "medium":
        incident.priority = "high"
    if incident.priority == "high":
        incident.priority = "critical"