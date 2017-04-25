from lib.util_sqlalchemy import ResourceMixin


from lib.util_sqlalchemy import AwareDateTime
from scoring.extensions import db


class Peer(ResourceMixin, db.Model):

    __tablename__ = 'peers'
    id = db.Column(db.Integer, primary_key=True)

    # Peer details
    ip = db.Column(db.String(128), index=True)
    mac = db.Column(db.String(128), index=True)
    alive = db.Column(db.Boolean(), nullable=False, server_default='0')
    last_request = db.Column(AwareDateTime(), nullable=True)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Peer, self).__init__(**kwargs)

    @classmethod
    def find_by_id(cls, id):
        """
        Return the peer by id

        :param id: peer id
        :return: peer
        """

        return Peer.query.filter(Peer.id == id).first()

    @classmethod
    def find_by_ip(cls, ip):
        """
        Return the peer by ip

        :param ip:
        :return: peer
        """

        return Peer.query.filter(Peer.ip == ip).first()

    @classmethod
    def get_all_peers(cls):
        """
        Return a list of all alive peers

        :return: list of peers
        """

        return Peer.query.all()

    @classmethod
    def get_alive_peers(cls):
        """
        Return a list of all alive peers

        :return: list of peers
        """

        return Peer.query.filter(Peer.alive.is_(True)).all()

    @classmethod
    def get_most_dead_peer(cls):
        """
        Return the peer which didn't respond longest time ago.

        :return: peer
        """
        return Peer.query.filter(Peer.alive.is_(False)).order_by(Peer.updated_on).first()

    def to_json(self):
        """
        Return JSON fields to represent a peer

        :return: dict
        """

        params = {
            'ip': self.ip,
            'mac': self.mac,
            'alive': self.alive
        }

        return params

    @classmethod
    def insert_from_json(cls, json):
        """
        Insert a peer from a json object.
        Note: if a peer with same IP already exists, it will
        update that peer.

        :param json:
        :return:
        """
        peer = cls.find_by_ip(json['ip'])
        if peer is None:
            peer = Peer()
        peer.ip = json['ip']
        peer.mac = json['mac']
        peer.alive = True  # All new peers should initially be alive. The only become dead after failed request
        peer.save()
