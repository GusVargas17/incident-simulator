from incident.models import Incident

def sort_incidents_by_priority(incidents: list[Incident]) -> list[Incident]:
    """
    Sort a list of incidents so that high-priority ones come first.
    Priority levels: critical > high > medium > low
    """
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(incidents, key=lambda i: priority_order.get(i.priority, 99))