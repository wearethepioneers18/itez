import uuid


def generate_uuid_and_agent_code():
    """
    Generates a seven digit agent ID and a unique ID.
    """
    uu_id = uuid.uuid4()
    agent_code = str(uu_id)[1:8].upper()
    
    return uu_id, agent_code
