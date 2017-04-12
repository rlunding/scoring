import click
import random

from datetime import datetime, timedelta

from faker import Faker

from scoring.app import create_app
from scoring.extensions import db
from scoring.blueprints.user.models import User

# Create an app context for the database connection.
app = create_app()
db.app = app

fake = Faker()


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
def users():
    """
    Generate fake users.
    """
    random_emails = []
    data = []

    click.echo('Working...')

    # Ensure we get about 100 unique random emails.
    for i in range(0, 99):
        random_emails.append(fake.email())

    random_emails.append(app.config['SEED_ADMIN_EMAIL'])
    random_emails = list(set(random_emails))

    while True:
        if len(random_emails) == 0:
            break

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        created_on = datetime.utcfromtimestamp(
            float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        random_percent = random.random()

        if random_percent >= 0.03:
            role = 'member'
        else:
            role = 'admin'

        email = random_emails.pop()

        random_percent = random.random()

        if random_percent >= 0.05:
            fullname = fake.first_name() + " " + fake.last_name()
            room = int(random_percent * 100)
        else:
            fullname = None
            room = None

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        current_sign_in_on = datetime.utcfromtimestamp(
            float(fake_datetime)).strftime('%Y-%m-%dT%H:%M:%S Z')

        params = {
            'created_on': created_on,
            'updated_on': created_on,
            'role': role,
            'email': email,
            'fullname': fullname,
            'room': room,
            'password': User.encrypt_password('password'),
            'sign_in_count': random.random() * 100,
            'current_sign_in_on': current_sign_in_on,
            'current_sign_in_ip': fake.ipv4(),
            'last_sign_in_on': current_sign_in_on,
            'last_sign_in_ip': fake.ipv4()
        }

        # Ensure the seeded admin is always an admin with the seeded password.
        if email == app.config['SEED_ADMIN_EMAIL']:
            password = User.encrypt_password(app.config['SEED_ADMIN_PASSWORD'])

            params['role'] = 'admin'
            params['password'] = password

        data.append(params)

    return _bulk_insert(User, data, 'users')


@click.command()
def item_groups():
    """
    Generate item_groups
    """
    data = []

    # Create a fake unix timestamp in the future.
    created_on = fake.date_time_between(
        start_date='-30d', end_date='now').strftime('%s')
    created_on = datetime.utcfromtimestamp(
        float(created_on)).strftime('%Y-%m-%dT%H:%M:%S Z')

    titles = ['Rum', 'Vask']

    for i in range(0, len(titles)):

        params = {
            'created_on': created_on,
            'updated_on': created_on,
            'title': titles[i],
        }
        data.append(params)

    return _bulk_insert(ItemGroup, data, 'item_groups')


@click.command()
def items():
    """
    Generate items
    """
    data = []

    # Create a fake unix timestamp in the future.
    created_on = fake.date_time_between(
        start_date='-30d', end_date='now').strftime('%s')
    created_on = datetime.utcfromtimestamp(
        float(created_on)).strftime('%Y-%m-%dT%H:%M:%S Z')

    titles = ['Baren', 'Pejsestuen', 'Venstre vaskemaskine', 'Højre vaskemaskine']
    groups = [1, 1, 2, 2]

    for i in range(0, len(titles)):

        params = {
            'created_on': created_on,
            'updated_on': created_on,
            'title': titles[i],
            'rules': fake.text(max_nb_chars=500),
            'delete_day_offset': random.randint(7, 14),
            'group_id': groups[i],
        }
        data.append(params)

    return _bulk_insert(Item, data, 'items')


@click.command()
def reservations():
    """
    Generate random reservations
    """
    data = []

    users = db.session.query(User).all()

    for user in users:
        for i in range(0, random.randint(0, 1)):
            random_percent = random.random()
            if random_percent >= 0.75:
                start = '-30d'
                end = 'now'
            else:
                start = 'now'
                end = '+30d'
            # Create a fake unix timestamp in the future.
            created_on = fake.date_time_between(
                start_date='-30d', end_date='now').strftime('%s')
            start_date = fake.date_time_between(
                start_date=start, end_date=end).strftime('%s')
            # TODO: Bug, this doesn't give a date after start_date
            end_date = fake.date_time_between(
                start_date=start_date, end_date='+5h').strftime('%s')

            created_on = datetime.utcfromtimestamp(
                float(created_on)).strftime('%Y-%m-%dT%H:%M:%S Z')
            start_date = datetime.utcfromtimestamp(
                float(start_date)).strftime('%Y-%m-%dT%H:%M:%S Z')
            end_date = datetime.utcfromtimestamp(
                float(end_date)).strftime('%Y-%m-%dT%H:%M:%S Z')



            title = fake.sentence(nb_words=5, variable_nb_words=True)
            description = fake.text(max_nb_chars=500)
            expiring = False

            params = {
                'created_on': created_on,
                'updated_on': created_on,
                'user_id': user.id,
                'title': title,
                'description': description,
                'item_id': random.randint(1, 4),
                'start_date': start_date,
                'end_date': end_date,
                'is_expiring': expiring
            }
            data.append(params)

    return _bulk_insert(Reservation, data, 'reservations')


@click.command()
@click.pass_context
def all(ctx):
    """
    Generate all data.

    :param ctx:
    :return: None
    """
    ctx.invoke(users)
    ctx.invoke(item_groups)
    ctx.invoke(items)
    ctx.invoke(reservations)

    return None


cli.add_command(users)
cli.add_command(item_groups)
cli.add_command(items)
cli.add_command(reservations)
cli.add_command(all)
