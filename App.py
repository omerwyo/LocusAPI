import logging
import socket
from LocusAPI import app
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def default_route():
    # to actually redirect to our API Developer Documentation page
    return "Python Template"


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":

    # our scheduler function goes here: 
    # .... 

    logging.info("Starting application ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=5000)
