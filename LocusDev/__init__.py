from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import LocusDev.routes.admin
import LocusDev.routes.tag


# app.config['DATABASE_URL'] = 'sqlite:///users.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)



