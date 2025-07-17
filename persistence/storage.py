import os
import json
from incident.models import Incident
from typing import List
from datetime import datetime

# Path where JSON files are stored
RESOLVED_PATH = "data/resolved_incidents.json"
ESCALATED_PATH = "data/escalated_incidents.json"

# ----------------- #
# Format Conversion #
# ----------------- #

def incident_to_dict(incident: Incident) -> dict:
    """
    Converts an Incident object into a serializable dictionary.
    """
    return {
        "id": incident.id,
        "type": incident.type,
        "priority": incident.priority,
        "description": incident.description,
        "created_at": incident.created_at.isoformat(),
        "assigned_to": incident.assigned_to,
        "status": incident.status
    }

def dict_to_incident(data: dict) -> Incident:
    """
    Converts a dictionary into an Incident object.
    """
    return Incident(    
        id=data["id"],
        type=data["type"],
        priority=data["priority"],
        description=data["description"],
        created_at=datetime.fromisoformat(data["created_at"]),
        assigned_to=data.get("assigned_to"),
        status=data["status"]
    )

# --------------------- #
# Persistence functions #
# --------------------- #

def load_incident(file_path: str) -> List[Incident]:
    """
    Upload incidents from a JSON file. 
    If the file does not exist, it returns an empty list.
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [dict_to_incident(item) for item in data]

def save_incident(file_path: str, incident: Incident) -> None:
    """
    Saves a new incident to the corresponding JSON file.
    If the file does not exist, create it.
    """
    incidents = load_incident(file_path)
    incidents.append(incident)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([incident_to_dict(i) for i in incidents], f, indent=4)

# ----------------- #
# Public interfaces #
# ----------------- #

def save_resolved_incident(incident: Incident) -> None:
    """
    Saves a resolved incident to the corresponding file.
    """
    save_incident(RESOLVED_PATH, incident)

def load_resolved_incident() -> List[Incident]:
    """
    Returns all resolved incidents.
    """
    return load_incident(RESOLVED_PATH)

def save_escalated_incident(incident: Incident):
    """
    Saves a escalated incident to the corresponding file.
    """
    save_incident(ESCALATED_PATH, incident)

def load_escalated_incident() -> List[Incident]:
    """
    Returns all escalated incidents.
    """
    return load_incident(ESCALATED_PATH)