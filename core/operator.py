from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

@dataclass
class Operator:
    """ Represent a system operator who can manage incident"""
    name: str
    role: str
    specialties: List[str]  # Incident types this operator can hadle
    max_incidents: int = 3
    assigned_incident: List[str] = field(default_factory=list)
    available_at: datetime = field(default_factory=lambda: datetime.now())
    status: str = "available" # or busy

    def is_avaliable(self) -> bool:
        """
        Check if the operator is available to take a new incident.
        Conditions:
            - Status must be 'available'.
            - Incident count must be below max_incidents.
            - Current time must be past 'available_at'.
        """
        return (
            self.status.lower() == "available"
            and len(self.assigned_incident) < self.max_incidents
            and datetime.now() >= self.available_at
        )
    
    def assign_incident(self, incident_id: str, estimated_minutes: int) -> None:
        """
        Assign a new incident to this operator.
        Updates:
            - Adds incident ID.
            - Updates availability time.
            - Updates status if max is reached.
        """
        self.assigned_incident.append(incident_id)
        self.available_at = datetime.now() + timedelta(minutes=estimated_minutes)

        if len(self.assign_incident) >= self.max_incidents:
            self.status = "busy"

    def remove_incident(self, incident_id: str) -> None:
        """
        Remove a resolved incident and update status
        """
        if incident_id in self.assign_incident:
            self.assign_incident.remove(incident_id)
        if len(self.assign_incident) < self.max_incidents:
            self.status = "available"