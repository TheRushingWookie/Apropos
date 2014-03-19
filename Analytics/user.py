# Analytics
from main import *


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.Text)

    def __init__(self, ip):
        self.ip = ip

    def __repr__(self):
        return ip
