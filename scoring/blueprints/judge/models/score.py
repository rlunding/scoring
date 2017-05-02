import datetime
import pytz

from sqlalchemy import desc, func, or_
from lib.util_sqlalchemy import ResourceMixin, AwareDateTime

from scoring.extensions import db


class Score(ResourceMixin, db.Model):

    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    team_1_id = db.Column(db.Integer, db.ForeignKey('teams.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=False)
    team_1 = db.relationship('Team', primaryjoin='Team.id==Score.team_1_id', lazy='joined')

    team_2_id = db.Column(db.Integer, db.ForeignKey('teams.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=True)
    team_2 = db.relationship('Team', primaryjoin='Team.id==Score.team_2_id', lazy='joined')

    # Schedule details
    table = db.Column(db.Integer, nullable=False, index=True)
    score_1 = db.Column(db.Integer, nullable=False)
    score_2 = db.Column(db.Integer, nullable=True)
    start_date = db.Column(AwareDateTime(), nullable=False, index=True)
    end_date = db.Column(AwareDateTime(), nullable=True)
    # TODO: add schedule_id such that duplicate scores can be removed
    version = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Score, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, score_id):
        """
        Return score by score id

        :param score_id: score id
        :return: score
        """

        return Score.query.filter(Score.id == score_id).first()

    @classmethod
    def find_by_table_id(cls, table_id):
        """
        Return all schedules by table_id

        :param table_id: table id
        :return: schedules
        """

        return Score.query.filter(Score.table == table_id).order_by(desc(func.greatest(Score.score_1, Score.score_2))).all()

    @classmethod
    def find_by_team_id(cls, team_id):
        """
        Return all scores by team_id

        :param team_id: team id
        :return: scores
        """

        return Score.query.filter(or_(Score.team_1_id == team_id, Score.team_2_id == team_id))\
            .order_by(desc(Score.start_date)).all()

    @classmethod
    def last_update(cls):
        """
        Return timestamp for when the newest score was updated

        :return: timestamp
        """

        return Score.query.with_entities(Score.updated_on).order_by(desc(Score.updated_on)).first()[0]

    @classmethod
    def updates_after_timestamp(cls, timestamp):
        """
        Return all scores that have been updated after the timestamp

        :param timestamp: timestamp
        :return: scores
        """

        return Score.query.filter(Score.updated_on >= timestamp).order_by(desc(Score.updated_on)).all()

    def to_json(self):
        """
        Return JSON fields to represent a score

        :return: dict
        """
        params = {
            'id': self.id,
            'team_1_id': self.team_1_id,
            'team_2_id': self.team_2_id,
            'table': self.table,
            'score_1': self.score_1,
            'score_2': self.score_2,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'version': self.version,
            'created_on': self.created_on
        }

        return params

    @classmethod
    def insert_from_json(cls, json):
        """
        Insert a score from a json object

        :param json:
        :return:
        """
        score = cls.find_by_id(json['id'])
        if score is not None:
            if score.version >= json['version']:
                return
        else:
            score = Score()
            score.id = json['id']
        score.table = json['table']
        score.team_1_id = json['team_1_id']
        score.team_2_id = json.get('team_2_id', None)
        score.score_1 = json['score_1']
        score.score_2 = json.get('score_2', None)
        score.start_date = json.get('start_date', datetime.datetime.now(pytz.utc))
        score.end_date = json.get('end_date', datetime.datetime.now(pytz.utc))
        score.version = json['version']

        db.session.merge(score)
        db.session.commit()
