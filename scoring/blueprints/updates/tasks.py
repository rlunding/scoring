from scoring.app import create_celery_app
import requests
import json

from scoring.blueprints.updates.models.peer import Peer

celery = create_celery_app()


@celery.task()
def retrieve_new_scores():
    """
    Retrieve scores from peers

    :return: None
    """
    pass


def update_peer_status(ip):
    """
    Update the status of a peer

    :return:
    """

    peer = Peer.find_by_ip(ip)  # TODO: pick a random peer or last updated
    port = 5000
    url = 'http://%s:%s/ping' % (peer.ip, port)

    try:
        data = json.loads(requests.get(url).text)
    except:
        return None
    if data is not None:
        if data['success'] is True:

            peer.alive = True
            peer.save()

            return data['peers']
    return None
