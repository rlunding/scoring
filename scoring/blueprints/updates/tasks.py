from scoring.app import create_celery_app
import requests
import json

from scoring.blueprints.judge.models.score import Score
from scoring.blueprints.updates.models.peer import Peer

celery = create_celery_app()


@celery.task()
def pull_new_scores():
    """
    Pull scores from peers

    :return: None
    """
    print("Scores pulled from peers")


@celery.task()
def push_new_scores(score_id):
    """
    Push scores to peers

    :return: None
    """
    print("Pushing scores to peers")
    print(score_id)


@celery.task()
def update_peer_status(ip):
    """
    Update the status of a peer in our database. If th
    peer responds we set alive=true

    :return:
    """

    peer = Peer.find_by_ip(ip)  # TODO: pick a random peer or last updated
    port = 5000
    url = 'http://%s:%s/ping' % (peer.ip, port)

    try:
        data = json.loads(requests.get(url, timeout=1).text)
    except:
        return "Error response from %s" % peer.ip
    if data is not None:
        if data['success'] is True:
            # Set the pinged peer alive in our db
            peer.alive = True
            peer.save()
            return data['peers']
        return "Success not true in data"
    return "Data returned from %s was None" % peer.ip