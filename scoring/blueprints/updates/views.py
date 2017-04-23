import json
from flask import (
    jsonify,
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template)

from scoring.blueprints.updates.models.peer import Peer
import requests


updates = Blueprint('update', __name__, template_folder='templates')


@updates.route('/ping_test', methods=['GET'])
def ping_test():
    ip = '192.168.4.2'
    peer = Peer.find_by_ip(ip)  # TODO: pick a random peer or last updated
    if peer is None:
        return "No peer found in database"

    port = 5000
    url = 'http://%s:%s/pong' % (peer.ip, port)

    try:
        data = json.loads(requests.get(url, timeout=1).text)
    except:
        return "No response from %s" % peer.ip
    if data is not None:
        if data['success'] is True:

            peer.alive = True
            peer.save()

            return data['peers']
    return "Data returned from %s was None" % peer.ip


@updates.route('/ping', methods=['GET'])
def ping():
    """
    Respond to a ping with a list of known peers

    """
    db_peers = Peer.query.all()

    peer_array = []
    for peer in db_peers:
        json_peer = {'id': peer.id, 'ip': peer.ip, 'alive': peer.alive}
        peer_array.append(json_peer)

    return jsonify({
        'success': True,
        'peers': peer_array})
