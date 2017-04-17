from flask import Blueprint, render_template, redirect, url_for

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/home')
def home():
    return redirect(url_for('spectator.home'))
    #return render_template('page/home.html')


@page.route('/faq')
def faq():
    return render_template('page/faq.html')


@page.route('/about')
def about():
    return render_template('page/about.html')
