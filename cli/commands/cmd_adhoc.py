from scoring.blueprints.updates.tasks import update_peer_status
from scoring.blueprints.updates.tasks import read_peers_from_file
from scoring.blueprints.updates.tasks import write_peers_to_file
from scoring.blueprints.updates.tasks import update_peers_file

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


cli.add_command(ping)
cli.add_command(readfile)
cli.add_command(writefile)
cli.add_command(updatefile)

