from flask import Blueprint, render_template

judge = Blueprint('judge', __name__, template_folder='templates')


@judge.route('/judge')
def home():
    return render_template('home.html')
