from lib.util_sqlalchemy import ResourceMixin

from scoring.extensions import db


class Peer(ResourceMixin, db.Model):

    __tablename__ = 'peers'
    id = db.Column(db.Integer, primary_key=True)


    # Peer details
    ip = db.Column(db.String(128), index=True)
    mac = db.Column(db.String(128), index=True)
    alive = db.Column(db.Boolean(), nullable=False, server_default='0')


    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Peer, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id):
        """
        Return the team by id

        :param team_id: team id
        :return: team
        """

        return Peer.query.filter(Peer.id == id).first()
