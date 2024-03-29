import pytz
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app

from lib.util_datetime import tzware_datetime, timedelta
from scoring.blueprints.judge.models.team import Team, db
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score

from scoring.blueprints.judge.decorators import get_peers
from scoring.blueprints.judge.forms import MatchForm1Player, MatchForm2Players


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


judge = Blueprint('judge', __name__, template_folder='templates') #, url_prefix='/judge')


@judge.before_request
@get_peers
def before_request():
    #if request.remote_addr != current_app.config['SERVER_NAME']: #'172.26.0.1':
    #    flash('You are not allowed here!' + request.remote_addr, 'danger')
    #    return render_template('errors/403.html'), 403
    pass


@judge.route('/')
def home():
    return redirect(url_for('spectator.tables'))
    #return render_template('judge/home.html')


# Match ---------------------------------------------------------------------------
@judge.route('/match/<int:schedule_id>', methods=['GET', 'POST'])
def match(schedule_id):
    schedule = Schedule.find_by_id(schedule_id)
    if schedule is None:
        return render_template('errors/404.html'), 404

    if schedule.team_2_id is None:
        form = MatchForm1Player(obj=schedule)
        form.team_1_name.data = schedule.team_1.name
    else:
        form = MatchForm2Players(obj=schedule)
        form.team_1_name.data = schedule.team_1.name
        form.team_2_name.data = schedule.team_2.name

    if form.validate_on_submit():
        score = Score()
        form.populate_obj(score)
        score.id = schedule_id
        score.table = safe_cast(score.table, int, None)
        score.team_1_id = safe_cast(score.team_1_id, int, None)
        score.team_2_id = safe_cast(score.team_2_id, int, None)

        if schedule.completed or schedule.table != score.table or schedule.team_1_id != score.team_1_id or schedule.team_2_id != score.team_2_id:
            print(schedule.completed, schedule.table != score.table, schedule.team_1_id != score.team_1_id, schedule.team_2_id != score.team_2_id)
            return render_template('errors/500.html'), 500

        score.start_date = score.start_date.replace(tzinfo=pytz.UTC)
        score.end_date = score.end_date.replace(tzinfo=pytz.UTC)
        score.save()

        schedule.completed = True
        schedule.version += 1
        schedule.save()

        from scoring.blueprints.updates.tasks import push_new_scores
        push_new_scores.delay(score.id, None)

        flash('Scoring has been saved successfully.', 'success')
        return redirect(url_for('spectator.table', table_id=schedule.table))

    return render_template('judge/match.html',
                           schedule_id=schedule_id,
                           form=form)
