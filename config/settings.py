from datetime import timedelta

from celery.schedules import crontab


DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

SERVER_NAME = 'localhost:8000'
SECRET_KEY = 'insecurekeyfordev'

# Flask-Mail.
MAIL_DEFAULT_SENDER = 'contact@local.host'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'you@gmail.com'
MAIL_PASSWORD = 'awesomepassword'

# Flask-Babel.
LANGUAGES = {
    'en': 'English',
    'da': 'Danish'
}
BABEL_DEFAULT_LOCALE = 'en'

# Celery.
CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
CELERYBEAT_SCHEDULE = {
#    'mark-expired-reservations': {
#        'task': 'scoring.blueprints.reservation.tasks.mark_expired_reservations',
#        'schedule': crontab(hour=2, minute=0, day_of_week='sunday')
#    },
}

# SQLAlchemy.
db_uri = 'postgresql://scoring:devpassword@postgres:5432/scoring'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_EMAIL = 'lunding@me.com'
SEED_ADMIN_PASSWORD = 'password'
REMEMBER_COOKIE_DURATION = timedelta(days=90)

# Limitter.
RATELIMIT_STORAGE_URL = CELERY_BROKER_URL
RATELIMIT_STRATEGY = 'fixed-window-elastic-expiry'
RATELIMIT_HEADERS_ENABLED = True