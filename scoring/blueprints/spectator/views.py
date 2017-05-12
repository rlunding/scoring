from flask import Blueprint, render_template, redirect, url_for

from lib.util_datetime import tzware_datetime, timedelta
from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score

spectator = Blueprint('spectator', __name__, template_folder='templates')


# Home page -----------------------------------------------------------------------
@spectator.route('/')
def home():
    # Last scores
    # Search team
    # Search table
    #return render_template('spectator/home.html')
    return redirect(url_for('spectator.tables'))


# Tables --------------------------------------------------------------------------
@spectator.route('/table', methods=['GET'])
def tables():
    # TODO: this assumes that all table with scores also have a schedule-element
    #tables = db.session.query(Schedule.table).distinct().order_by(Schedule.table).all()
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