import uuid


def generate_uuid_and_agent_code():
    """
     This function generate a 7 digit code for agent.
    """
    uuid_one = uuid.uuid4()
    agent_code = str(uuid_one)[1:8].upper()
    return uuid_one, agent_code
