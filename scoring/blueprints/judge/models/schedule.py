from sqlalchemy import desc
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
    #team_1 = db.relationship('Team', backref='parents', lazy='joined')
    team_2_id = db.Column(db.Integer, db.ForeignKey('teams.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=True)
    #team_2 = db.relationship('Team', backref='parents', lazy='joined')

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
