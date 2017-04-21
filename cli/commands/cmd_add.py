import click
import random

from datetime import datetime, timedelta

from faker import Faker

from scoring.app import create_app
from scoring.extensions import db
from scoring.blueprints.judge.models.team import Team
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score
from scoring.blueprints.updates.models.peer import Peer

# Create an app context for the database connection.
app = create_app()
db.app = app

fake = Faker()

RANDOM_TEAMS = 30
RANDOM_SCHEDULES_PR_TEAM = 10
TABLES = 10


def _log_status(count, model_label):
    """
    Log the output of how many records were created.

    :param count: Amount created
    :type count: int
    :param model_label: Name of the model
    :type model_label: str
    :return: None
    """
    click.echo('Created {0} {1}'.format(count, model_label))

    return None


def _bulk_insert(model, data, label):
    """
    Bulk insert data to a specific model and log it. This is much more
    efficient than adding 1 row at a time in a loop.

    :param model: Model being affected
    :type model: SQLAlchemy
    :param data: Data to be saved
    :type data: list
    :param label: Label for the output
    :type label: str
    :param skip_delete: Optionally delete previous records
    :type skip_delete: bool
    :return: None
    """
    with app.app_context():
        model.query.delete()

        db.session.commit()
        db.engine.execute(model.__table__.insert(), data)

        _log_status(model.query.count(), label)

    return None


@click.group()
def cli():
    """ Add items to the database. """
    pass


@click.command()
def teams():
    """
    Generate fake teams.
    """
    click.echo('Working...')
    data = []

    for i in range(0, RANDOM_TEAMS):
        params = {
            'name': fake.first_name()
        }

        data.append(params)

    return _bulk_insert(Team, data, 'teams')


@click.command()
def schedules():
    """
    Generate fake schedules.
    """
    click.echo('Working...')
    data = []

    teams = db.session.query(Team).all()

    for team in teams:
        for i in range(0, random.randint(0, RANDOM_SCHEDULES_PR_TEAM)):
            start_date = fake.date_time_between(
                    start_date='-3h', end_date='+5h').strftime('%s')
            start_date = datetime.utcfromtimestamp(
                float(start_date)).strftime('%Y-%m-%dT%H:%M:%S Z')

            params = {
                'team_1_id': team.id,
                'team_2_id': None,
                'table': random.randint(1, TABLES),
                'start_date': start_date,
                'completed': random.choice([True, False])
            }

            data.append(params)

    if RANDOM_TEAMS > 10:
        for (t1, t2) in zip(teams[::2], teams[1::2]):
            start_date = fake.date_time_between(
                start_date='-3h', end_date='+5h').strftime('%s')
            start_date = datetime.utcfromtimestamp(
                float(start_date)).strftime('%Y-%m-%dT%H:%M:%S Z')

            params = {
                'team_1_id': t1.id,
                'team_2_id': t2.id,
                'table': TABLES+1,
                'start_date': start_date,
                'completed': random.choice([True, False])
            }

            data.append(params)

    return _bulk_insert(Schedule, data, 'schedules')


@click.command()
def scores():
    """
    Generate fake scores.
    """
    click.echo('Working...')
    data = []

    teams = db.session.query(Team).all()

    for team in teams:
        for i in range(0, random.randint(0, 3)):
            start_date = fake.date_time_between(
                start_date='-1h', end_date='now').strftime('%s')
            start_date = datetime.utcfromtimestamp(
                float(start_date)).strftime('%Y-%m-%dT%H:%M:%S Z')

            params = {
                'team_1_id': team.id,
                'team_2_id': None,
                'table': random.randint(1, TABLES),
                'start_date': start_date,
                'score_1': random.randint(0, 200),
                'score_2': None
            }

            data.append(params)

    if RANDOM_TEAMS > 10:
        for (t1, t2) in zip(teams[::2], teams[1::2]):
            start_date = fake.date_time_between(
                start_date='-1h', end_date='now').strftime('%s')
            start_date = datetime.utcfromtimestamp(
                float(start_date)).strftime('%Y-%m-%dT%H:%M:%S Z')

            params = {
                'team_1_id': t1.id,
                'team_2_id': t2.id,
                'table': TABLES+1,
                'start_date': start_date,
                'score_1': random.randint(0, 200),
                'score_2': random.randint(0, 200)
            }

            data.append(params)

    return _bulk_insert(Score, data, 'scores')

@click.command()
def peers():
    """
    Generate peers.
    """
    click.echo('Adding peers...')

    data = []
    params = {
        'ip': '192.168.4.2',
        'mac': 'b8:27:eb:7f:8c:f3',
        'alive': False
    }
    data.append(params)

    return _bulk_insert(Peer, data, 'peers')

@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(teams)
    ctx.invoke(schedules)
    ctx.invoke(scores)
    ctx.invoke(peers)

    return None


cli.add_command(teams)
cli.add_command(schedules)
cli.add_command(scores)
cli.add_command(peers)
cli.add_command(all)
