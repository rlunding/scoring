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

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Score, self).__init__(**kwargs)

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
        Return timestamp for the newest score

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
            'team_1_id': self.team_1_id,
            'team_2_id': self.team_2_id,
            'table': self.table,
            'score_1': self.score_1,
            'score_2': self.score_2,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

        return params
