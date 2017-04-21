from subprocess import call
import requests

import click


@click.command()
@click.argument('ip')
def ping(ip):
    """
    Show hostname

    :return: str
    """

    #return click.echo(call(["ping", "-c", "5", "192.168.0.101"]))

    click.echo('Ping: %s' % ip)
    pong = requests.get('http://%s:5000/scores' % ip).content
    click.echo(pong)

    return None
