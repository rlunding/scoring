import requests
import json
import datetime
import pytz

from lib.util_datetime import timedelta
from scoring.app import create_celery_app

from scoring.blueprints.judge.models.team import Team
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score
from scoring.blueprints.updates.models.peer import Peer

celery = create_celery_app()


@celery.task()
def pull_new_updates():
    """
    Pull updates from peers

    :return: None
    """
    # Get alive peer(s)
    # send pull-request (with latest timestamp)
    # loop through response

    print("Pulling updates from peers....")
    for peer in Peer.get_alive_peers():
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
            print("Response: ", request.text)
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
        except:
            print("Ill-formatted JSON response")

    print("Updates pulled from peers")


@celery.task()
def push_new_updates(score_id):
    """
    Push updates to peers

    :return: None
    """
    print("Pushing updates to peers")
    print(score_id)


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
        # Set the pinged peer alive in our db
        peer.alive = True
        peer.save()
        if data:
            # Insert new peers in db
            for json_peer in data['peers']:
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
            mac = peer[1]

            json_peer = {
                'ip': ip,
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
        string += peer.ip + ' ' + peer.mac + '\n'

    filename = 'adhoc.txt'
    with open(filename, 'w') as f:
        f.write(string)


