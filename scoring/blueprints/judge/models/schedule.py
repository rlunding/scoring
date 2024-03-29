import datetime
import pytz

from sqlalchemy import desc, asc, and_, or_, func
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
    version = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Schedule, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, schedule_id):
        """
        Return schedule by schedule id

        :param schedule_id: schedule id
        :return: schedule
        """

        return Schedule.query.filter(Schedule.id == schedule_id).first()

    @classmethod
    def find_by_table_id(cls, table_id):
        """
        Return all schedules by table_id

        :param table_id: table id
        :return: schedules
        """

        return Schedule.query.filter(Schedule.table == table_id).order_by(desc(Schedule.start_date)).all()

    @classmethod
    def get_random_row(cls):
        """
        Return a random schedule that haven't been completed

        :return: schedule
        """
        return Schedule.query.filter(Schedule.completed.is_(False)).order_by(func.random()).first()

    @classmethod
    def find_by_team_id(cls, team_id):
        """
        Return all schedules by team_id

        :param team_id: team id
        :return: schedules
        """

        return Schedule.query.filter(or_(Schedule.team_1_id == team_id, Schedule.team_2_id == team_id))\
            .order_by(desc(Schedule.start_date)).all()

    @classmethod
    def find_next_by_team_id(cls, team_id):
        """
        Return next schedule for a team, given a team_id

        :param team_id: team id
        :return: schedule
        """

        now = datetime.datetime.now(pytz.utc)

        next_schedule = Schedule.query\
            .with_entities(Schedule.start_date)\
            .filter(and_(or_(Schedule.team_1_id == team_id, Schedule.team_2_id == team_id), Schedule.start_date >= now, Schedule.completed.is_(False)))\
            .order_by(asc(Schedule.start_date)).first()
        if next_schedule:
            return next_schedule[0]
        else:
            return None

    @classmethod
    def last_update(cls):
        """
        Return timestamp for when the newest schedule was updated

        :return: timestamp
        """

        schedule = Schedule.query.with_entities(Schedule.updated_on).order_by(desc(Schedule.updated_on)).first()
        if schedule:
            return schedule[0]
        else:
            return None

    @classmethod
    def get_all_tables(cls):
        """
        Return a list of all tables

        :return:
        """
        return Schedule.query.with_entities(Schedule.table).distinct().order_by(Schedule.table).all()

    @classmethod
    def updates_after_timestamp(cls, timestamp):
        """
        Return all schedules that have been updated after the timestamp

        :param timestamp: timestamp
        :return: schedules
        """

        return Schedule.query.filter(Schedule.updated_on >= timestamp).order_by(desc(Schedule.updated_on)).all()

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
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'completed': self.completed,
            'version': self.version
        }

        return params

    @classmethod
    def insert_from_json(cls, json):
        """
        Insert a schedule from a json object

        :param json:
        :return:
        """
        schedule = cls.find_by_id(json['id'])
        if schedule is not None:
            if schedule.version >= json['version']:
                return
        else:
            schedule = Schedule()
            schedule.id = json['id']
        schedule.table = json['table']
        schedule.team_1_id = json['team_1_id']
        schedule.team_2_id = json.get('team_2_id', None)
        schedule.start_date = json.get('start_date', datetime.datetime.now(pytz.utc))
        schedule.end_date = json.get('end_date', datetime.datetime.now(pytz.utc))
        schedule.completed = json['completed']
        schedule.version = json['version']

        db.session.merge(schedule)
        db.session.commit()
