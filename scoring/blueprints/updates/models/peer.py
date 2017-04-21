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
        Return the peer by id

        :param id: team id
        :return: peer
        """

        return Peer.query.filter(Peer.id == id).first()

    @classmethod
    def find_by_ip(cls, ip):
        """
        Return the peer by ip

        :param ip:
        :return:
        """

        return Peer.query.filter(Peer.ip == ip).first()
