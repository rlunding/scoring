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
    #team_1 = db.relationship('Team', backref='parents', lazy='joined')
    team_2_id = db.Column(db.Integer, db.ForeignKey('teams.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=True)
    #team_2 = db.relationship('Team', backref='parents', lazy='joined')

    # Schedule details
    table = db.Column(db.Integer, nullable=False, index=True)
    score_1 = db.Column(db.Integer, nullable=False)
    score_2 = db.Column(db.Integer, nullable=True)
    start_date = db.Column(AwareDateTime(), nullable=False, index=True)
    end_date = db.Column(AwareDateTime(), nullable=True)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Score, self).__init__(**kwargs)
