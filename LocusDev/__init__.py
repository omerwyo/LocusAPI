from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

import LocusDev.routes.admin
import LocusDev.routes.tag

app = Flask(__name__)

# app.config['DATABASE_URL'] = 'sqlite:///users.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)




