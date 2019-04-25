from app import api
from sqlalchemy.dialects.postgresql import JSONB 

db = api.db

matches = db.Table(
    'matches',
    db.Column('summoner_id', db.BigInteger, db.ForeignKey('summoner.id'), primary_key=True),
    db.Column('match_id', db.BigInteger, db.ForeignKey('match.id'), primary_key=True)
)

class Summoner(db.Model):
    __tablename__ = 'summoner'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    account_id = db.Column(db.BigInteger)
    lp = db.Column(db.Integer)
    rank = db.Column(db.String)
    level = db.Column(db.Integer)
    matches = db.relationship('Match', secondary=matches, lazy='subquery', backref=db.backref('summoner', lazy=True))
    
class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.BigInteger, primary_key=True)
    datetime = db.Column(db.DateTime)
    info = db.Column(JSONB)
    timeline = db.Column(JSONB)

