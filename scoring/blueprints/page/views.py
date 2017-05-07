from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    current_app)

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
