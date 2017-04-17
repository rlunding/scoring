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
