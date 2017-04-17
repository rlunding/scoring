from flask import Blueprint, render_template

from lib.util_datetime import tzware_datetime, timedelta
from scoring.blueprints.judge.models.team import Team
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score

spectator = Blueprint('spectator', __name__, template_folder='templates')


# Home page -----------------------------------------------------------------------
@spectator.route('/')
def home():
    # Last scores
    # Search team
    # Search table
    return render_template('home.html')


# Tables --------------------------------------------------------------------------
@spectator.route('/table', methods=['GET'])
def tables():
    # All tables
    pass


@spectator.route('/table/<int:table_id>', methods=['GET'])
def table(table_id):
    # Last 5 scores
    # Next 5 matches
    # Teams
    pass


@spectator.route('/table/<int:table_id>/schedule', methods=['GET'])
def schedule(table_id):
    # Show full schedule for table
    current_time = tzware_datetime()
    schedules = Schedule.find_by_table_id(table_id)
    return render_template('spectator/schedule.html', schedules=schedules, current_time=current_time)


@spectator.route('/table/<int:table_id>/score', methods=['GET'])
def score(table_id):
    # Show full scoring for table
    current_time_offset = timedelta(minutes=-10)
    scores = Score.find_by_table_id(table_id)
    return render_template('spectator/scoring.html', scores=scores, current_time_offset=current_time_offset)


# Teams ---------------------------------------------------------------------------
@spectator.route('/team/<int:team_id>')
def team(team_id):
    # Show team information
    team = Team.find_by_id(team_id)
    if team is None:
        return render_template('errors/404.html'), 404
    current_time = tzware_datetime()
    current_time_offset = timedelta(minutes=-10)
    schedules = Schedule.find_by_team_id(team_id)
    scores = Score.find_by_team_id(team_id)
    return render_template('spectator/team.html',
                           team=team,
                           current_time=current_time,
                           current_time_offset=current_time_offset,
                           schedules=schedules,
                           scores=scores)
