import logging
from flask import Flask, redirect
from scraper import scheduler
import os
from models import db

app = Flask(__name__)

app.config['DATABASE_URL'] =  os.environ.get('DATABASE_URL')
# app.config['DATABASE_URL'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()



logger = logging.getLogger(__name__)
@app.route('/', methods=['GET'])
def default_route():
    # the homepage redirects to our API Developer Documentation page
    return redirect("https://dev.locus.social/")

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":

    # our scheduler function goes here:
    scheduler.start()
    logging.info("Starting application ...")
    app.run(debug=False, port=33507)
