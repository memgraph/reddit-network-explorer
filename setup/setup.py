#!/usr/bin/python3

from gqlalchemy import Memgraph
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable
from time import sleep


KAFKA_ENDPOINT = 'kafka:9092'


def get_admin_client():
    retries = 30
    while True:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=KAFKA_ENDPOINT,
                client_id="reddit-stream")
            return admin_client
        except NoBrokersAvailable:
            retries -= 1
            if not retries:
                raise
            print("Failed to connect to Kafka")
            sleep(1)


def main():
    admin_client = get_admin_client()
    print("Connected to Kafka")

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
    print("Created topics")

    print("Connecting to Memgraph")
    memgraph = Memgraph()
    print("Creating stream connections on Memgraph")
    memgraph.execute(
        "CREATE STREAM comment_stream TOPICS comments TRANSFORM reddit.comments")
    memgraph.execute("START STREAM comment_stream")
    memgraph.execute(
        "CREATE STREAM submission_stream TOPICS submissions TRANSFORM reddit.submissions")
    memgraph.execute("START STREAM submission_stream")

    print("Creating triggers on Memgraph")
    memgraph.execute(
        "CREATE TRIGGER created_trigger ON CREATE AFTER COMMIT EXECUTE CALL publisher.create(createdObjects)")


if __name__ == "__main__":
    main()
