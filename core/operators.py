from core.operator import Operator
from typing import Dict

OPERATORS: Dict[str, Operator] = {
    "Alice": Operator(
        name="Alice",
        role="support_level_1",
        specialties=["network", "software"],
        max_incidents=2
    ),
    "Carlos": Operator(
        name="Carlos",
        role="admin",
        specialties=["all"],
        max_incidents=5
    ),
    "Max": Operator(
        name="Max",
        role="support_level_2",
        specialties=["hardware", "database", "software"],
        max_incidents=2
    ),
    "Dana": Operator(
        name="Dana",
        role="support_level_1",
        specialties=["software", "ux"],
        max_incidents=2
    ),
    "Eric": Operator(
        name="Eric",
        role="support_level_2",
        specialties=["security", "network"],
        max_incidents=3
    ),
}