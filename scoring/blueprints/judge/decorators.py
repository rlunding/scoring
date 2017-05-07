from functools import wraps

from flask import g

from scoring.blueprints.updates.models.peer import Peer


def get_peers(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        peers = getattr(g, '_peers', None)
        if peers is None:
            g._peers = Peer.get_all_peers()
        return f(*args, **kwargs)
    return decorated_function
