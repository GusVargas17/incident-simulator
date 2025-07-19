current_id = 1

def generate_incident_id() -> str:
    """
    Generates IDs for incidents for example: 001, 002, etc
    """
    global current_id
    id_str = f"{current_id:03}"
    current_id += 1
    return id_str