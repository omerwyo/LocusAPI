import logging
import socket
from LocusDev import app, db
from flask import redirect
from scraper import scheduler

logger = logging.getLogger(__name__)
@app.route('/', methods=['GET'])
def default_route():
    # to actually redirect to our API Developer Documentation page
    return redirect("https://omerwyo.gitbook.io/locusapi/")
    # return "Welcome to Locus.io"

class Article(db.Model):
    __tablename__='articles'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    datePosted = db.Column(db.Date)
    bodyText = db.Column(db.Text)
    minutesToRead = db.Column(db.Integer)


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
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind(('localhost', 0))
    # port = sock.getsockname()[1]
    # sock.close()
    # db.create_all()
    app.run(debug=False, port=33507)
