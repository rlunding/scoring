from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request)
from sqlalchemy import text

from lib.util_datetime import tzware_datetime, timedelta
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score
from scoring.blueprints.judge.models.team import Team
from scoring.blueprints.spectator.forms import SearchForm

spectator = Blueprint('spectator', __name__, template_folder='templates')


# Home page -----------------------------------------------------------------------
@spectator.route('/')
def home():
    return redirect(url_for('spectator.tables'))


@spectator.route('/faq')
def faq():
    return render_template('spectator/faq.html')


@spectator.route('/about')
def about():
    return render_template('spectator/about.html')


# Tables --------------------------------------------------------------------------
@spectator.route('/table', methods=['GET'])
def tables():
    tables = Schedule.get_all_tables()
    return render_template('spectator/tables.html', tables=tables)


@spectator.route('/table/<int:table_id>', methods=['GET'])
def table(table_id):
    current_time = tzware_datetime()
    current_time_offset = timedelta(minutes=-10)
    schedules = Schedule.find_by_table_id(table_id)
    scores = Score.find_by_table_id(table_id)
    return render_template('spectator/table.html',
                           table_id=table_id,
                           current_time=current_time,
                           current_time_offset=current_time_offset,
                           schedules=schedules,
                           scores=scores)


@spectator.route('/table/<int:table_id>/schedule', methods=['GET'])
def schedule(table_id):
    # Show full schedule for table
    current_time = tzware_datetime()
    schedules = Schedule.find_by_table_id(table_id)
    return render_template('spectator/schedule.html',
                           table_id=table_id,
                           schedules=schedules,
                           current_time=current_time)


@spectator.route('/table/<int:table_id>/score', methods=['GET'])
def score(table_id):
    # Show full scoring for table
    current_time_offset = timedelta(minutes=-10)
    scores = Score.find_by_table_id(table_id)
    return render_template('spectator/scoring.html',
                           table_id=table_id,
                           scores=scores,
                           current_time_offset=current_time_offset)


# Teams ---------------------------------------------------------------------------
@spectator.route('/teams', defaults={'page': 1})
@spectator.route('/teams/page/<int:page>')
def teams(page):
    search_form = SearchForm()

    sort_by = Team.sort_by(request.args.get('sort', 'name'),
                           request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_teams = Team.query \
        .filter(Team.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 20, True)

    return render_template('spectator/teams.html',
                           form=search_form,
                           teams=paginated_teams)


@spectator.route('/teams/<int:team_id>', methods=['GET'])
def team(team_id):
    # Show team information
    team = Team.find_by_id(team_id)
    if team is None:
        return render_template('errors/404.html'), 404
    current_time = tzware_datetime()
    current_time_offset = timedelta(minutes=-10)
    schedules = Schedule.find_by_team_id(team_id)
    scores = Score.find_by_team_id(team_id)
    next_schedule = Schedule.find_next_by_team_id(team_id)
    return render_template('spectator/team.html',
                           team=team,
                           current_time=current_time,
                           current_time_offset=current_time_offset,
                           next_schedule=next_schedule,
                           schedules=schedules,
                           scores=scores)
