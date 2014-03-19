from main import *


class api_analytic(db.Model):
    __tablename__ = 'api_analytics'
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api_endpoints.id'))
    api = db.relationship(
        "api_endpoints", backref=db.backref('api_analytics', order_by=id))
