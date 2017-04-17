from flask import Blueprint, render_template

spectator = Blueprint('spectator', __name__, template_folder='templates')


@spectator.route('/spectator')
def home():
    return render_template('home.html')
