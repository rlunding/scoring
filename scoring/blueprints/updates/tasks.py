import requests
import json
import datetime
import pytz

from flask import current_app

from lib.util_datetime import timedelta
from scoring.app import create_celery_app

from scoring.blueprints.judge.models.team import Team
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score
from scoring.blueprints.updates.models.peer import Peer
from scoring.blueprints.updates.models.log import Log
from scoring.blueprints.updates.communication import sign_json, verify_json

celery = create_celery_app()


@celery.task()
def pull_new_updates():
    """
    Pull updates from peers

    Get alive peer(s)
    Send pull-request (with latest timestamp from that peer)
    Loop through response (potentially adding: teams, schedules, and scores)

    :return: None
    """
    printed_header = False

    for peer in Peer.get_alive_peers():
        if peer.ip+":"+str(peer.port) == current_app.config['SERVER_NAME']:  # Check if peer is itself
            continue

        if not printed_header: # Print header to console
            print("Pulling updates from peers....")
            printed_header = True

        last_request = peer.last_request
        if last_request is None:
            last_request = timedelta(weeks=-10)

        url = 'http://%s:%s/pull_data/%s' % (peer.ip, peer.port, last_request.isoformat())
        print("Contacting: %s" % url)

        try:
            request = requests.get(url, timeout=1)
        except:
            peer.alive = False
            peer.save()
            continue

        if request.status_code != 200:
            print("Error response from %s. Status code: %s" % (peer.ip, request.status_code))
            continue
        try:
            data = json.loads(request.text)

            peer.last_request = data['time']
            peer.save()

            for json_data in data['teams']:
                Team.insert_from_json(json_data)

            for json_data in data['schedules']:
                Schedule.insert_from_json(json_data)

            for json_data in data['scores']:
                Score.insert_from_json(json_data)
                # Log
                Log.log_score(json_data, peer.ip)
        except:
            print("Ill-formatted JSON response")

    if printed_header:
        print("Updates pulled from peers")
    else:
        print("No updates pulled from peers...")


@celery.task()
def push_new_scores(score_id, peer_list):
    """
    Push scores to peers

    All peers are optimistic informed about which peers we have pushed the information too.

    :return: None
    """
    print("Pushing scores to peers")

    score = Score.find_by_id(score_id).to_json()  # Retrieve the score and convert it to json
    alive_peers = Peer.get_alive_peers(peer_list)  # Get alive peers that haven't received the message
    peers = [peer.mac for peer in alive_peers]  # Get mac addresses
    output_json = {
        'score': score,
        'peers': peers + (peer_list if peer_list is not None else []),  # Combine lists of peers
    }
    output_json['signature'] = sign_json(output_json)

    for peer in alive_peers:
        if peer.ip+":"+str(peer.port) == current_app.config['SERVER_NAME']:  # Check if peer is itself
            continue

        url = 'http://%s:%s/push_data' % (peer.ip, peer.port)
        try:
            request = requests.post(url, timeout=1, json=output_json)
        except:
            print("Error response from %s:%s. Likely timeout." % (peer.ip, peer.port))
            peer.alive = False
            peer.save()
            continue

        if request.status_code != 200:
            print("Error response from %s. Status code: %s. Message: %s" % (peer.ip, request.status_code, request.text))
        else:
            print("Successfully pushed to: %s" % peer.ip)
    print("Success")


@celery.task()
def update_peer_status(ip):
    """
    Update the status of a peer in our database. If the
    peer responds we set alive=true. Otherwise alive=false.

    Also inserts new peers in db from the ping response.

    :return:
    """

    if ip is None:
        peer = Peer.get_most_dead_peer()
    else:
        peer = Peer.find_by_ip(ip)

    if peer is None:
        return "Peer not found"
    url = 'http://%s:%s/ping' % (peer.ip, peer.port)

    try:
        request = requests.get(url, timeout=1)
    except:
        peer.alive = False
        peer.updated_on = datetime.datetime.now(pytz.utc)
        peer.save()
        return "Error response from %s:%s. Likely timeout." % (peer.ip, peer.port)

    if request.status_code != 200:
        return "Error response from %s:%s. Status code: %s" % (peer.ip, peer.port, request.status_code)
    try:
        data = json.loads(request.text)

        if data:
            # Check signature
            if not (verify_json(data['peers'], data['signature'])):
                return "Wrong signature on peers"

            # Set the pinged peer alive in our db
            peer.alive = True
            peer.save()

            # Insert new peers in db
            for json_peer in json.loads(data['peers']):
                Peer.insert_from_json(json_peer)
            return data['peers']
        return "Data returned from %s was None" % peer.ip
    except:
        return "Ill-formatted JSON response"


@celery.task()
def update_peers_file():
    """
    Update adhoc.txt file by inserting entries to db
    and also writing db to the file afterwards.

    """
    read_peers_from_file()
    write_peers_to_file()


@celery.task()
def read_peers_from_file():
    """
    Read adhoc.txt file and initialize database
    with peers from it.

    """
    filename = 'adhoc.txt'
    with open(filename, 'r') as f:
        for line in f:
            peer = line.split()
            ip = peer[0]
            port = int(peer[1])
            mac = peer[2]

            json_peer = {
                'ip': ip,
                'port': port,
                'mac': mac
            }
            Peer.insert_from_json(json_peer)


@celery.task()
def write_peers_to_file():
    """
    Write peers from database into the adhoc.txt
    file.

    """
    string = ''
    for peer in Peer.get_all_peers():
        string += peer.ip + ' ' + str(peer.port) + ' ' + peer.mac + '\n'

    filename = 'adhoc.txt'
    with open(filename, 'w') as f:
        f.write(string)
