import eventlet
import json
import logging
import os
import server.setup as setup
import time
import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from argparse import ArgumentParser
from eventlet import greenthread
from flask import Flask, render_template, Response
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from functools import wraps
from kafka import KafkaConsumer, KafkaProducer

eventlet.monkey_patch()

KAFKA_IP = os.getenv('KAFKA_IP', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'created_objects')
MEMGRAPH_IP = os.getenv('MEMGRAPH_IP', 'memgraph-mage')
MEMGRAPH_PORT = os.getenv('MEMGRAPH_PORT', '7687')

logging.getLogger("kafka").setLevel(logging.ERROR)
log = logging.getLogger(__name__)


def init_log():
    logging.basicConfig(level=logging.DEBUG)
    log.info("Logging is enabled")
    logging.getLogger("werkzeug").setLevel(logging.WARNING)


"""
def parse_args():
    parser = ArgumentParser(
        description="A Reddit explorer powered by Memgraph.")
    parser.add_argument("--host", default="0.0.0.0", help="Host address.")
    parser.add_argument("--port", default=5000, type=int, help="App port.")
    parser.add_argument(
        "--debug",
        default=True,
        action="store_true",
        help="Start the Flask server in debug mode.",
    )
    return parser.parse_args()


args = parse_args()
"""
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
cors = CORS(app)
memgraph = None


def set_up_memgraph_and_kafka():
    global memgraph
    memgraph = setup.connect_to_memgraph(MEMGRAPH_IP, MEMGRAPH_PORT)
    setup.run(memgraph, KAFKA_IP, KAFKA_PORT)

    def old_node_deleter():
        node_limit = datetime.datetime.utcnow() - datetime.timedelta(days=4)
        delete_info = {
            'timestamp': int(node_limit.timestamp())
        }
        producer = KafkaProducer(bootstrap_servers=KAFKA_IP + ':' + KAFKA_PORT)
        producer.send('node_deleter', json.dumps(delete_info).encode('utf8'))
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=old_node_deleter, trigger='interval', hours=1)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())


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


def parse_node(result):
    node = None
    if list(result.labels)[0] == "SUBMISSION":
        node = {
            'id': result.id,
            'labels': list(result.labels),
            'title': result.properties['title'],
            'sentiment': result.properties['sentiment']
        }

    if list(result.labels)[0] == "COMMENT":
        node = {
            'id': result.id,
            'labels': list(result.labels),
            'body': result.properties['body'],
            'sentiment': result.properties['sentiment']
        }

    if list(result.labels)[0] == "REDDITOR":
        node = {
            'id': result.id,
            'labels': list(result.labels),
            'name': result.properties['name'],
        }
    return node


@app.route("/api/graph", methods=["GET"])
@cross_origin()
def get_graph():
    results = list(memgraph.execute_and_fetch("""
        match (n)-[r]-(m:REDDITOR) return n, r, m order by n.created_at desc limit 30
    """))

    nodes_id_set = set()
    links_id_set = set()
    nodes_list = []
    links_list = []
    for result in results:
        source = parse_node(result['n'])
        target = parse_node(result['m'])
        edge = {
            'id': result['r'].id,
            'type': result['r'].type,
            'from': source['id'],
            'to': target['id'],
        }

        if source['id'] not in nodes_id_set:
            nodes_id_set.add(source['id'])
            nodes_list.append(source)
        if target['id'] not in nodes_id_set:
            nodes_id_set.add(target['id'])
            nodes_list.append(target)
        if edge['id'] not in links_id_set:
            links_id_set.add(edge['id'])
            links_list.append(edge)

    response = {"vertices": nodes_list, "edges": links_list}
    return Response(json.dumps(response), status=200, mimetype="application/json")


@socketio.on('connect')
def test_connect():
    emit('logs', {'data': 'Connection established'})


def kafkaconsumer():
    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=KAFKA_IP + ':' + KAFKA_PORT)
    try:
        while True:
            msg_pack = consumer.poll()
            if not msg_pack:
                greenthread.sleep(1)
                continue
            for _, messages in msg_pack.items():
                for message in messages:
                    message = json.loads(message.value.decode('utf8'))
                    log.info("Message: " + str(message))
                    try:
                        socketio.emit('consumer', {'data': message})
                    except Exception as error:
                        log.info(f"`{message}`, {repr(error)}")
                        continue
    except KeyboardInterrupt:
        pass


@app.before_first_request
def execute_this():
    init_log()
    set_up_memgraph_and_kafka()
    greenthread.spawn(kafkaconsumer)

"""
def main():
    # if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    init_log()
    set_up_memgraph_and_kafka()
    greenthread.spawn(kafkaconsumer)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
"""