import click
import random
from time import sleep

from datetime import datetime, timedelta

from faker import Faker

from lib.contry_code_converter import get_country
from lib.uuid import generate_uuid
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
RANDOM_SCHEDULES_PR_TEAM = 15
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
        country_code = fake.country_code()
        params = {
            'id': generate_uuid(),
            'name': fake.first_name(),
            'country': get_country(country_code),
            'country_code': country_code
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
                'id': generate_uuid(),
                'team_1_id': team.id,
                'team_2_id': None,
                'table': random.randint(1, TABLES),
                'start_date': start_date,
                'completed': False  # random.choice([True, False])
            }

            data.append(params)

    if RANDOM_TEAMS > 10:
        for (t1, t2) in zip(teams[::2], teams[1::2]):
            start_date = fake.date_time_between(
                start_date='-3h', end_date='+5h').strftime('%s')
            start_date = datetime.utcfromtimestamp(
                float(start_date)).strftime('%Y-%m-%dT%H:%M:%S Z')

            params = {
                'id': generate_uuid(),
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
                'id': generate_uuid(),
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
                'id': generate_uuid(),
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
    click.echo('Working...')
    data = []

    params = {
        'ip': '192.168.4.2',
        'port': 5000,
        'mac': 'b8:27:eb:7f:8c:f3',
        'alive': False
    }
    data.append(params)
    params = {
        'ip': '192.168.4.4',
        'port': 5000,
        'mac': 'b8:27:eb:3c:dc:97',
        'alive': False
    }
    data.append(params)
    params = {
        'ip': '192.168.42.1',
        'port': 8000,
        'mac': 'b8:27:eb:3c:dc:97',
        'alive': True
    }
    data.append(params)

    return _bulk_insert(Peer, data, 'peers')


@click.command()
@click.argument('times', int)
def scores_pull(times):
    """
    Slowly add some scores
    """
    click.echo("Adding some scores slowly")
    for x in range(0, int(times)):
        # Add score
        schedule = Schedule.get_random_row()

        params = {
            'id': schedule.id,
            'team_1_id': schedule.team_1_id,
            'team_2_id': schedule.team_2_id,
            'table': schedule.table,
            'start_date': schedule.start_date,
            'score_1': random.randint(0, 200),
            'score_2': 0,
            'version': schedule.version
        }
        Score.insert_from_json(params)
        click.echo("Score added")

        schedule.completed = True
        schedule.version += 1
        schedule.save()
        click.echo("Schedule updated. Table: %s" % schedule.table)

        # Wait
        rand = random.randint(1, 5)
        click.echo("Waiting %s seconds..." % rand)
        sleep(rand)

    return click.echo("Adding scores slowly is completed")


@click.command()
@click.argument('times', int)
def scores_push(times):
    """
    Slowly push some scores
    """
    click.echo("Pushing some scores slowly")
    for x in range(0, int(times)):
        # Add score
        schedule = Schedule.get_random_row()

        params = {
            'id': schedule.id,
            'team_1_id': schedule.team_1_id,
            'team_2_id': schedule.team_2_id,
            'table': schedule.table,
            'start_date': schedule.start_date,
            'score_1': random.randint(0, 200),
            'score_2': 0,
            'version': schedule.version
        }
        score = Score.insert_from_json(params)
        click.echo("Score added")

        schedule.completed = True
        schedule.version += 1
        schedule.save()
        click.echo("Schedule updated. Table: %s" % schedule.table)

        from scoring.blueprints.updates.tasks import push_new_scores
        push_new_scores.delay(score.id, None)
        click.echo("Score pushed to peers")

        # Wait
        rand = random.randint(1, 5)
        click.echo("Waiting %s seconds..." % rand)
        sleep(rand)

    return click.echo("Adding scores slowly is completed")


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


@click.command()
@click.pass_context
def prepare_test(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(teams)
    ctx.invoke(schedules)

    return None


cli.add_command(teams)
cli.add_command(schedules)
cli.add_command(scores)
cli.add_command(scores_pull)
cli.add_command(peers)
cli.add_command(all)
cli.add_command(scores_push)
cli.add_command(prepare_test)
