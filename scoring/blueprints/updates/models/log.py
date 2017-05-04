import datetime
import pytz
from lib.util_sqlalchemy import ResourceMixin
from flask import current_app


from lib.util_sqlalchemy import AwareDateTime
from scoring.extensions import db


class Log(ResourceMixin, db.Model):

    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)

    # Logging details
    ip_sender = db.Column(db.String(128), index=True)
    ip_receiver = db.Column(db.String(128), index=True)
    timestamp_sender = db.Column(AwareDateTime(), nullable=True)
    timestamp_receiver = db.Column(AwareDateTime(), nullable=True)
    type = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128), nullable=True)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Log, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id):
        """
        Return the peer by id

        :param id: peer id
        :return: peer
        """

        return Log.query.filter(Log.id == id).first()

    @classmethod
    def get_all_logs(cls):
        """
        Return a list of all alive peers

        :return: list of peers
        """

        return Log.query.all()

    def to_json(self):
        """
        Return JSON fields to represent a log entry

        :return: dict
        """

        params = {
            'ip_sender': self.ip_sender,
            'ip_receiver': self.ip_receiver,
            'timestamp_sender': self.timestamp_sender,
            'timestamp_receiver': self.timestamp_receiver,
            'type': self.type,
            'description': self.description,
        }

        return params

    @classmethod
    def store_from_json(cls, json):
        """
        
        :param json:
        :return:
        """

        log = Log()
        log.ip_sender = json['ip_sender']
        log.ip_receiver = json['ip_receiver']
        log.timestamp_sender = json['timestamp_sender']
        log.timestamp_receiver = datetime.datetime.now(pytz.utc).isoformat()
        log.type = json['type']
        log.description = json['description']
        log.save()

    @classmethod
    def log_score(cls, json, ip_sender):
        """
        Log a received score entry.
         
        """
        print('Logging Score: %s' % json)
        log = Log()
        log.ip_sender = ip_sender
        log.ip_receiver = current_app.config['SERVER_NAME']
        log.timestamp_sender = json['created_on']
        log.timestamp_receiver = datetime.datetime.now(pytz.utc).isoformat()
        log.type = 'score_received'
        log.description = json['id']
        log.save()
        print('Score logged')

    @classmethod
    def log_timestamp(cls, json):
        """
        Log a received timestamp message
        
        :param json: 
        :return: 
        """

        log = Log()
        log.ip_sender = json['ip']
        log.ip_receiver = current_app.config['SERVER_NAME']
        log.timestamp_sender = json['timestamp']
        log.timestamp_receiver = datetime.datetime.now(pytz.utc).isoformat()
        log.type = 'timestamp_received'
        log.save()
