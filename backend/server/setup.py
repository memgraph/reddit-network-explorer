import logging
from gqlalchemy import Memgraph
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable
from pathlib import Path
from time import sleep


log = logging.getLogger(__name__)


def connect_to_memgraph(memgraph_ip, memgraph_port):
    memgraph = Memgraph(host=memgraph_ip, port=int(memgraph_port))
    while(True):
        try:
            if (memgraph._get_cached_connection().is_active()):
                return memgraph
        except:
            log.info("Memgraph probably isn't running.")
            sleep(1)


# TODO: Change data import query and add import files to /memgraph/import-data
def import_data(memgraph):
    """Load data into the database."""
    try:
        path = Path("/usr/lib/memgraph/import-data/import_file.csv")

        memgraph.execute_query(
            f"""LOAD CSV FROM "{path}"
            WITH HEADER DELIMITER " " AS row"""
        )
    except Exception as e:
        log.error("Error while loading data:\n" + e)


def get_admin_client(kafka_ip, kafka_port):
    retries = 30
    while True:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=kafka_ip + ':' + kafka_port,
                client_id="reddit-stream")
            return admin_client
        except NoBrokersAvailable:
            retries -= 1
            if not retries:
                raise
            log.info("Failed to connect to Kafka")
            sleep(1)


def run(memgraph, kafka_ip, kafka_port):
    admin_client = get_admin_client(kafka_ip, kafka_port)
    log.info("Connected to Kafka")

    topic_list = [
        NewTopic(
            name="comments",
            num_partitions=1,
            replication_factor=1),
        NewTopic(
            name="submissions",
            num_partitions=1,
            replication_factor=1),
        NewTopic(
            name="created_objects",
            num_partitions=1,
            replication_factor=1)]

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except TopicAlreadyExistsError:
        pass
    log.info("Created topics")

    memgraph.drop_database()
    log.info("Creating stream connections on Memgraph")
    memgraph.execute(
        "CREATE STREAM comment_stream TOPICS comments TRANSFORM reddit.comments")
    memgraph.execute("START STREAM comment_stream")
    memgraph.execute(
        "CREATE STREAM submission_stream TOPICS submissions TRANSFORM reddit.submissions")
    memgraph.execute("START STREAM submission_stream")

    log.info("Creating triggers on Memgraph")
    memgraph.execute(
        "CREATE TRIGGER created_trigger ON CREATE AFTER COMMIT EXECUTE CALL publisher.create(createdObjects)")
