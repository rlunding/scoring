from sqlalchemy import desc, or_
from lib.util_sqlalchemy import ResourceMixin, AwareDateTime

from scoring.extensions import db


class Schedule(ResourceMixin, db.Model):

    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    team_1_id = db.Column(db.Integer, db.ForeignKey('teams.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=False)
    team_1 = db.relationship('Team', primaryjoin='Team.id==Schedule.team_1_id', lazy='joined')

    team_2_id = db.Column(db.Integer, db.ForeignKey('teams.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=True)
    team_2 = db.relationship('Team', primaryjoin='Team.id==Schedule.team_2_id', lazy='joined')

    # Schedule details
    table = db.Column(db.Integer, nullable=False)
    start_date = db.Column(AwareDateTime(), nullable=False, index=True)
    end_date = db.Column(AwareDateTime(), nullable=True)
    completed = db.Column(db.Boolean(), nullable=False, server_default='0')

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Schedule, self).__init__(**kwargs)

    @classmethod
    def find_by_table_id(cls, table_id):
        """
        Return all schedules by table_id

        :param table_id: table id
        :return: schedules
        """

        return Schedule.query.filter(Schedule.table == table_id).order_by(desc(Schedule.start_date)).all()

    @classmethod
    def find_by_team_id(cls, team_id):
        """
        Return all schedules by team_id

        :param team_id: team id
        :return: schedules
        """

        return Schedule.query.filter(or_(Schedule.team_1_id == team_id, Schedule.team_2_id == team_id))\
            .order_by(desc(Schedule.start_date)).all()
