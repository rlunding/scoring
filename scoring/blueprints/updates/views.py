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
    render_template,
    current_app)

from lib.util_json import render_json

from scoring.blueprints.judge.models.team import Team
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score
from scoring.blueprints.updates.models.peer import Peer
from scoring.blueprints.updates.models.log import Log
from scoring.blueprints.updates.communication import sign_json, verify_json, datetime_handler


updates = Blueprint('update', __name__, template_folder='templates')


@updates.route('/timestamp', methods=['GET'])
def timestamp():
    return render_json(200, {
        'ip': current_app.config['SERVER_NAME'],
        'timestamp': datetime.datetime.now(pytz.utc).isoformat()
    })


@updates.route('/log', methods=['GET'])
def all_log_entries():

    db_log = Log.get_all_logs()
    log_array = []
    for log in db_log:
        log_array.append(log.to_json())

    return render_json(200, {
        'success': True,
        'logs': log_array})

@updates.route('/log/<string:type>', methods=['GET'])
def log_entries_by_type(type):

    db_log = Log.get_all_logs_by_type(type)
    log_array = []
    for log in db_log:
        log_array.append(log.to_json())

    return render_json(200, {
        'success': True,
        'logs': log_array})



@updates.route('/ping', methods=['GET'])
def ping():
    """
    Respond to a ping with a list of known peers

    """
    db_peers = Peer.get_all_peers()

    peer_array = []
    for peer in db_peers:
        peer_array.append(peer.to_json())

    peers_json = json.dumps(peer_array)
    signature = sign_json(peers_json)

    return render_json(200, {
        'success': True,
        'peers': peers_json,
        'signature': signature})


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


@updates.route('/push_data', methods=['POST'])
def push():
    print(request.json)
    if not request.json:
        return render_json(406, {'error': 'Mime-type is not application/json'})
    if 'signature' not in request.json or request.json.get('signature') is None:
        return render_json(406, {'error': 'Signature are not set'})
    if 'data' not in request.json or request.json.get('data') is None:
        return render_json(406, {'error': 'Data are not set'})
    if not (verify_json(json.dumps(request.json.get('data')), request.json.get('signature'))):
        return render_json(406, {'error': 'Signature not correct'})

    data = request.json.get('data')
    score_json = data['score']
    peer_list = data['peers']

    schedule = Schedule.find_by_id(score_json['id'])
    if schedule is None:
        return render_json(406, {'error': 'Unknown schedule'})
    try:
        score = Score.insert_from_json(score_json)
        if score:
            schedule.completed = True
            schedule.version += 1
            schedule.save()

            from scoring.blueprints.updates.tasks import push_new_scores
            push_new_scores.delay(score.id, peer_list)

        print("Score pushed from peer", request.json)
    except Exception as e:
        return render_json(500, {'error': str(e)})

    return render_json(200, {'success': True})
