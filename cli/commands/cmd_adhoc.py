from subprocess import call
import requests

import click

@click.group()
def cli():
    """ Run adhoc related tasks. """
    pass


@click.command()
@click.argument('ip')
def ping(ip):
    """
    Show hostname

    :return: str
    """

    #return click.echo(call(["ping", "-c", "5", "192.168.0.101"]))

    click.echo('Ping: %s' % ip)
    pong = requests.get('http://%s:5000/ping' % ip).content
    click.echo(pong)

    return None

cli.add_command(ping)
