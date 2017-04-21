from subprocess import call
import requests

import click


@click.command()
def cli():
    """
    Show hostname

    :return: str
    """

    #return click.echo(call(["ping", "-c", "5", "192.168.0.101"]))
    return click.echo(requests.get('192.168.4.2:5000/scores').content)
