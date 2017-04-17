from flask import Blueprint, render_template

from lib.util_datetime import tzware_datetime
from scoring.blueprints.judge.models.schedule import Schedule

spectator = Blueprint('spectator', __name__, template_folder='templates')


@spectator.route('/spectator')
def home():
    return render_template('home.html')


@spectator.route('/schedule/<int:table>', methods=['GET'])
def schedule(table):
    current_time = tzware_datetime()
    schedules = Schedule.find_by_table_id(table)
    return render_template('schedule.html', schedules=schedules, current_time=current_time)
