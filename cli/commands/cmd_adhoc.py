from scoring.blueprints.updates.tasks import update_peer_status
from scoring.blueprints.updates.tasks import read_peers_from_file
from scoring.blueprints.updates.tasks import write_peers_to_file
from scoring.blueprints.updates.tasks import update_peers_file
from scoring.blueprints.updates.communication import verify_json
from scoring.blueprints.updates.communication import sign_json
from scoring.blueprints.updates.tasks import timestamp_test

import ntplib
from time import ctime
import requests
import json

from random import randint
from time import sleep

import click


@click.group()
def cli():
    """ Run adhoc related tasks. """
    pass


@click.command()
@click.argument('ip')
def ping(ip):
    """
    Ping a peer using ip

    """

    click.echo('Ping: %s' % ip)
    pong = update_peer_status(ip)
    click.echo(pong)
    return None


@click.command()
def readfile():
    """
    Read adhoc.txt file and initialize database
    with peers from it.

    :return:
    """

    return click.echo(read_peers_from_file())


@click.command()
def writefile():
    """
    Write peers from database into the adhoc.txt
    file.

    :return:
    """

    return click.echo(write_peers_to_file())


@click.command()
def updatefile():
    """
    Update adhoc.txt file by inserting entries to db
    and also writing db to the file afterwards.
    :return:
    """

    update_peers_file()
    return click.echo('Peer database and file updated')

@click.command()
def time():
    """
    Get NTP time

    :return:
    """

    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org')
    click.echo('Offset: %s' % response.offset)
    click.echo(ctime(response.tx_time))
    return None


@click.command()
@click.argument('ip')
@click.argument('times', int)
def timestamp(ip, times):
    """
    Send timestamp to ip for time sync testing
    
    :param ip: 
    :return: 
    """
    click.echo("Doing %s timestamp tests on: %s" % (times, ip))
    for x in range(0, int(times)+1):
        # Do timestamp test
        click.echo(timestamp_test(ip))

        # Wait
        rand = randint(1, 5)
        click.echo("Waiting %s seconds..." % rand)
        sleep(rand)

    return click.echo("Timestamp test done")

@click.command()
def test_signature():
    """
    Just a command for testing

    :return:
    """
    url = 'http://%s:%s/ping' % ('localhost', '8000')

    try:
        request = requests.get(url, timeout=6)
    except:
        return click.echo("Error response from locals. Likely timeout.")

    try:
        data = json.loads(request.text)

        if data:
            # Check signature
            new_sig = sign_json(data['peers'])
            click.echo(json.dumps(data['peers']))
            click.echo(data['signature'])
            click.echo(new_sig)
            click.echo(verify_json(data['peers'], data['signature']))

            # Insert new peers in db
            for json_peer in json.loads(data['peers']):
                click.echo(json_peer)

            return data['peers']
        return click.echo("Data returned from %s was None")
    except:
        return click.echo("eeor")

cli.add_command(ping)
cli.add_command(readfile)
cli.add_command(writefile)
cli.add_command(updatefile)
cli.add_command(time)
cli.add_command(test_signature)
cli.add_command(timestamp)
