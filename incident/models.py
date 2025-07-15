from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Incident:
    id: int
    type: str
    priority: str
    description: str
    created_at: datetime
    assigned_to: Optional[str] = None
    status: str = "pending"