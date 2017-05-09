from lib.util_sqlalchemy import ResourceMixin

from sqlalchemy import desc
from scoring.extensions import db

# Do not delete this imports
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

    # Team details
    name = db.Column(db.String(128), index=True)
    version = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Team, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, team_id):
        """
        Return the team by id

        :param team_id: team id
        :return: team
        """

        return Team.query.filter(Team.id == team_id).first()

    @classmethod
    def last_update(cls):
        """
        Return timestamp for when the newest team was updated

        :return: timestamp
        """
        team = Team.query.with_entities(Team.updated_on).order_by(desc(Team.updated_on)).first()
        if team:
            return team[0]
        else:
            return None

    @classmethod
    def updates_after_timestamp(cls, timestamp):
        """
        Return all teams that have been updated after the timestamp

        :param timestamp: timestamp
        :return: scores
        """

        return Team.query.filter(Team.updated_on >= timestamp).order_by(desc(Team.updated_on)).all()

    def to_json(self):
        """
        Return JSON fields to represent a team

        :return: dict
        """

        params = {
            'id': self.id,
            'name': self.name,
            'version': self.version
        }

        return params

    @classmethod
    def insert_from_json(cls, json):
        """
        Insert a team from a json object

        :param json:
        :return:
        """
        team = cls.find_by_id(json['id'])
        if team is not None:
            if team.version >= json['version']:
                return
        else:
            team = Team()
            team.id = json['id']
        team.name = json['name']
        team.version = json['version']

        db.session.merge(team)
        db.session.commit()
