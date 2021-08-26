from argparse import ArgumentParser
from kafka import KafkaProducer
import json
from time import sleep


KAFKA_ENDPOINT = 'kafka:9092'


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


def main():
    args = parse_args()

    producer = KafkaProducer(bootstrap_servers=KAFKA_ENDPOINT)
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
