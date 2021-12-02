import uuid


def generate_uuid():
    """
    Generates a seven digit agent ID and a unique ID.
    """
    unique_id = uuid.uuid4()
    agent_code = f"Agent-{str(unique_id)[1:8].upper()}"
    beneficiary_code = f"Beneficiary-{str(unique_id)[1:8].upper()}"
    
    return beneficiary_code, agent_code
