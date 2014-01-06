from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getcwd() + '/API.db'
logger = app.logger
db = SQLAlchemy(app)