from subprocess import call
import requests

from scoring.blueprints.updates.tasks import update_peer_status
from scoring.blueprints.updates.models.peer import Peer

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

    #return click.echo(call(["ping", "-c", "5", "192.168.0.101"]))

    click.echo('Ping: %s' % ip)
    #pong = requests.get('http://%s:5000/ping' % ip).content

    pong = update_peer_status(ip)

    click.echo(pong)

    return None

@click.command()
@click.argument('ip')
def peer(ip):
    """
    Get a peer

    """

    peer = Peer.find_by_ip(ip)
    click.echo(peer.id)
    click.echo(peer.mac)

    return None


cli.add_command(ping)
cli.add_command(peer)
