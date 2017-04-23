from scoring.blueprints.updates.tasks import update_peer_status

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

cli.add_command(ping)

