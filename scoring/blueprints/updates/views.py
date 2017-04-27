import datetime
import dateutil.parser
import pytz
import json
from flask import (
    jsonify,
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template)

from lib.util_json import render_json

from scoring.blueprints.judge.models.team import Team
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score
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
    db_peers = Peer.get_all_peers()

    peer_array = []
    for peer in db_peers:
        peer_array.append(peer.to_json())

    return render_json(200, {
        'success': True,
        'peers': peer_array})


@updates.route('/pull_data/<string:timestamp>', methods=['GET'])
def pull(timestamp):
    if timestamp is None:  # Check timestamp
        return render_json(412, {'error': 'Timestamp not provided'})

    try:
        timestamp_validated = dateutil.parser.parse(timestamp)
    except Exception as e:
        return render_json(400, {'error': 'Timestamp ill formatted'})

    try:
        teams = [team.to_json() for team in Team.updates_after_timestamp(timestamp_validated)]
        schedules = [schedule.to_json() for schedule in Schedule.updates_after_timestamp(timestamp_validated)]
        scores = [score.to_json() for score in Score.updates_after_timestamp(timestamp_validated)]

        return render_json(200, {
            'teams': teams,
            'schedules': schedules,
            'scores': scores,
            'time': datetime.datetime.now(pytz.utc).isoformat(),
            'timestamp': timestamp_validated.isoformat(),
            'teams_last_update': Team.last_update().isoformat(),
            'schedules_last_update': Schedule.last_update().isoformat(),
            'scores_last_update': Score.last_update().isoformat(),
            'teams_updates': len(teams),
            'schedule_updates': len(schedules),
            'score_updates': len(scores)
        })
    except Exception as e:
        return render_json(500, {'error': str(e)})
