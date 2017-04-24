import uuid


def generate_uuid():
    """
    Generate a random string
    :return:
    """
    return uuid.uuid4().int & (1 << 31)-1
