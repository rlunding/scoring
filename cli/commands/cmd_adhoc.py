from subprocess import call

import click


@click.command()
def cli():
    """
    Show hostname

    :return: str
    """

    return click.echo(call(["ping", "-c", "5", "192.168.0.101"]))
