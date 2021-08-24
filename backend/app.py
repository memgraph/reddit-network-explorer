import logging
import time
from argparse import ArgumentParser
from flask import Flask
from functools import wraps
from pathlib import Path
from gqlalchemy import Memgraph


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


memgraph = Memgraph()


def connect_to_memgraph():
    connection_established = False
    while(not connection_established):
        try:
            if (memgraph._get_cached_connection().is_active()):
                connection_established = True
        except:
            log.info("Memgraph probably isn't running.")
            time.sleep(4)


app = Flask(__name__)


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        log.info(f"Time for {func.__name__} is {duration}")
        return result
    return wrapper


# TODO: Add data import query
@log_time
def import_data():
    """Load data into the database."""
    try:
        memgraph.drop_database()
        path = Path("/usr/lib/memgraph/import-data/karate_club.csv")

        memgraph.execute_query(
            f"""LOAD CSV FROM "{path}"
            WITH HEADER DELIMITER " " AS row"""
        )
    except Exception as e:
        log.error("Error while loading data:\n" + e)


@app.route("/", methods=["GET"])
def index():
    # import_data()
    return "<p>Hello, ssWorld!</p>"


def main():
    init_log()
    args = parse_args()
    connect_to_memgraph()
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
