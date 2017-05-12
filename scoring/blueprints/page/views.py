from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    current_app,
    request)
from sqlalchemy import text

from lib.util_datetime import tzware_datetime, timedelta
from scoring.blueprints.page.forms import SearchForm
from scoring.blueprints.judge.models.team import Team
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/home')
def home():
    if current_app.config['SCORING_APP_TYPE'] == 'JUDGE':
        return redirect(url_for('judge.home'))
    return redirect(url_for('spectator.home'))
    #return render_template('page/home.html')


@page.route('/faq')
def faq():
    return render_template('page/faq.html')


@page.route('/about')
def about():
    return render_template('page/about.html')


# Teams ---------------------------------------------------------------------------
@page.route('/teams', defaults={'page': 1})
@page.route('/teams/page/<int:page>')
def teams(page):
    search_form = SearchForm()

    sort_by = Team.sort_by(request.args.get('sort', 'name'),
                           request.args.get('direction', 'asc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_teams = Team.query \
        .filter(Team.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate(page, 20, True)

    return render_template('page/teams.html',
                           form=search_form,
                           teams=paginated_teams)


@page.route('/teams/<int:team_id>', methods=['GET'])
def team(team_id):
    # Show team information
    team = Team.find_by_id(team_id)
    if team is None:
        return render_template('errors/404.html'), 404
    current_time = tzware_datetime()
    current_time_offset = timedelta(minutes=-10)
    schedules = Schedule.find_by_team_id(team_id)
    scores = Score.find_by_team_id(team_id)
    return render_template('page/team.html',
                           team=team,
                           current_time=current_time,
                           current_time_offset=current_time_offset,
                           schedules=schedules,
                           scores=scores)
