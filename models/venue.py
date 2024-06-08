from config import db


class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(4000), nullable=True)
    type = db.Column(db.String(20), nullable=False)
    iconNum = db.Column(db.Integer, default=1)
