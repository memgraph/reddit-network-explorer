import json
import os
from argparse import ArgumentParser
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from time import sleep


KAFKA_IP = os.getenv('KAFKA_IP', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')


def parse_args():
    """
    Parse input command line arguments.
    """
    parser = ArgumentParser(
        description="A Reddit subreddit stream machine powered by Memgraph.")
    parser.add_argument("--file", help="File with subreddit data.")
    parser.add_argument(
        "--interval",
        type=int,
        help="Interval for sending data in seconds.")
    return parser.parse_args()


def create_kafka_producer():
    retries = 30
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_IP + ':' + KAFKA_PORT)
            return producer
        except NoBrokersAvailable:
            retries -= 1
            if not retries:
                raise
            print("Failed to connect to Kafka")
            sleep(1)


def main():
    args = parse_args()

    producer = create_kafka_producer()
    with open(args.file) as f:
        for line in f.readlines():
            line_json = json.loads(line)

            topic = 'submissions' if line_json['label'] == 'SUBMISSION' else 'comments'
            del line_json['label']

            print(f'Sending data to {topic}')
            producer.send(topic, json.dumps(line_json).encode('utf8'))
            sleep(args.interval)


if __name__ == "__main__":
    main()
