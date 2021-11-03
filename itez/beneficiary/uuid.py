import uuid


def generate_id():
    """
     this function generate a 7 digit code for agent
    """
    uuid_one = uuid.uuid4()
    print(uuid_one)
    agent_code = str(uuid_one)[1:8].upper()
    return (agent_code)
