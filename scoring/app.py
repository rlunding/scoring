import logging
from logging.handlers import SMTPHandler

from flask import Flask, render_template, request
from werkzeug.contrib.fixers import ProxyFix
from celery import Celery
from itsdangerous import URLSafeTimedSerializer

from scoring.blueprints.judge import judge
from scoring.blueprints.spectator import spectator
from scoring.blueprints.updates import updates

from scoring.blueprints.judge.models.team import Team

from lib.template_processors import (
    current_year
)
from scoring.extensions import (
    debug_toolbar,
    mail,
    csrf,
    db,
    limiter,
    babel
)

CELERY_TASK_LIST = [
    'scoring.blueprints.updates.tasks',
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_background_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('spectator.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    middleware(app)
    error_templates(app)
    exception_handler(app)
    # app.register_blueprint(page)
    # app.register_blueprint(judge)
    app.register_blueprint(spectator)
    # app.register_blueprint(updates)
    template_processors(app)
    extensions(app)
    locale(app)

    return app


def create_judge_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('judge.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    middleware(app)
    error_templates(app)
    exception_handler(app)
    # app.register_blueprint(page)
    app.register_blueprint(judge)
    app.register_blueprint(spectator)
    # app.register_blueprint(updates)
    template_processors(app)
    extensions(app)
    locale(app)

    return app


def create_background_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('updates.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    middleware(app)
    # error_templates(app)
    exception_handler(app)
    # app.register_blueprint(page)
    # app.register_blueprint(judge)
    # app.register_blueprint(spectator)
    app.register_blueprint(updates)
    # template_processors(app)
    extensions(app)
    # locale(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    babel.init_app(app)

    return None


def template_processors(app):
    """
    Register 0 or more custom template processors (mutates the app passed in).

    :param app: Flask application instance
    :return: App jinja environment
    """
    app.jinja_env.globals.update(current_year=current_year)

    return app.jinja_env


def locale(app):
    """
    Initialize a locale for the current request.

    :param app: Flask application instance
    :return: str
    """

    if babel.locale_selector_func is not None:
        return

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('LANGUAGES').keys()
        return request.accept_languages.best_match(accept_languages)


def middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Swap request.remote_addr with the real IP address even if behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None


def error_templates(app):
    """
    Register 0 or more custom error pages (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """

    def render_status(status):
        """
         Render a custom template for a specific status.
           Source: http://stackoverflow.com/a/30108946

         :param status: Status as a written name
         :type status: str
         :return: None
         """
        # Get the status code from the status, default to a 500 so that we
        # catch all types of errors and treat them as a 500.
        code = getattr(status, 'code', 500)
        return render_template('errors/{0}.html'.format(code)), code

    for error in [401, 403, 404, 405, 429, 500]:
        app.errorhandler(error)(render_status)

    return None


def exception_handler(app):
    """
    Register 0 or more exception handlers (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail_handler = SMTPHandler((app.config.get('MAIL_SERVER'),
                                app.config.get('MAIL_PORT')),
                               app.config.get('MAIL_USERNAME'),
                               [app.config.get('MAIL_USERNAME')],
                               '[Exception handler] A 5xx was thrown',
                               (app.config.get('MAIL_USERNAME'),
                                app.config.get('MAIL_PASSWORD')),
                               secure=())

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter("""
    Time:               %(asctime)s
    Message type:       %(levelname)s


    Message:

    %(message)s
    """))
    app.logger.addHandler(mail_handler)

    return None
