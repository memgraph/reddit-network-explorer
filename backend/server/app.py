import logging
import os
import pickle
import setup
import time
from argparse import ArgumentParser
from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from functools import wraps
from kafka import KafkaConsumer

KAFKA_IP = os.getenv('KAFKA_IP', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'created_objects')
MEMGRAPH_IP = os.getenv('MEMGRAPH_IP', 'memgraph-mage')
MEMGRAPH_PORT = os.getenv('MEMGRAPH_PORT', '7687')

log = logging.getLogger(__name__)


def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging is enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


def parse_args():
    """
    Parse input command line arguments.
    """
    parser = ArgumentParser(description="A Reddit explorer powered by Memgraph.")
    parser.add_argument("--host", default="0.0.0.0", help="Host address.")
    parser.add_argument("--port", default=5000, type=int, help="App port.")
    parser.add_argument(
        "--debug",
        default=True,
        action="store_true",
        help="Start the Flask server in debug mode.",
    )
    return parser.parse_args()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log.info(f"Time for {func.__name__} is {duration}")
        return result
    return wrapper


@app.route("/test", methods=["GET"])
@cross_origin()
def index():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    emit('logs', {'data': 'Connection established'})


@socketio.on('consumer')
def kafkaconsumer():
    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=KAFKA_IP+':'+KAFKA_PORT)
    try:
        for message in consumer:
            message = pickle.loads(message.value)
            log.info("Message: " + str(message))
            try:
                emit('consumer', {'data': str(message)})
            except Exception as error:
                logging.error(f"`{message}`, {repr(error)}")
                continue
    except KeyboardInterrupt:
        pass


def main():
    init_log()
    args = parse_args()

    memgraph = setup.connect_to_memgraph(MEMGRAPH_IP, MEMGRAPH_PORT)
    setup.run(memgraph, KAFKA_IP, KAFKA_PORT)

    socketio.run(app, host=args.host, port=args.port, debug=args.debug, use_reloader=False)


if __name__ == "__main__":
    main()
