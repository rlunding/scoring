from lib.util_sqlalchemy import ResourceMixin

from scoring.extensions import db

from scoring.blueprints.judge.models.schedule import Schedule
from scoring.blueprints.judge.models.score import Score


class Team(ResourceMixin, db.Model):

    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    schedules = db.relationship('Schedule', primaryjoin='or_(Team.id==Schedule.team_1_id, Team.id==Schedule.team_2_id)',
                                lazy='dynamic')
    scores = db.relationship('Score', primaryjoin='or_(Team.id==Score.team_1_id, Team.id==Score.team_2_id)',
                                lazy='dynamic')
    #schedules = db.relationship(Schedule, backref='schedules', passive_deletes=True)
    #scores = db.relationship(Score, backref='scores', passive_deletes=True)

    # Team details
    name = db.Column(db.String(128), index=True)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Team, self).__init__(**kwargs)
