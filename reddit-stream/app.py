import os
import praw
import json
from argparse import ArgumentParser
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from multiprocessing import Process
from time import sleep


KAFKA_IP = os.getenv('KAFKA_IP', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')


def parse_args():
    """
    Parse input command line arguments.
    """
    parser = ArgumentParser(
        description="A Reddit subreddit stream machine powered by Memgraph.")
    parser.add_argument("--subreddit", help="Subreddit to be scraped.")
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


def produce_comments(reddit, subreddit):
    producer = create_kafka_producer()

    print("Processing comments")
    for comment in reddit.subreddit(
            subreddit).stream.comments(skip_existing=True):
        comment_info = {
            'id': comment.id,
            'body': comment.body,
            'created_at': comment.created_utc,
            'redditor': {
                'id': comment.author.id,
                'name': comment.author.name
            },
            'parent_id': comment.parent_id[3:]}
        print("Sending a new comment")
        print(comment_info)
        producer.send('comments', json.dumps(comment_info).encode('utf8'))


def produce_submissions(reddit, subreddit):
    producer = create_kafka_producer()

    print("Processing submissions")
    for submission in reddit.subreddit(
            subreddit).stream.submissions(skip_existing=True):
        submission_info = {
            'id': submission.id,
            'title': submission.title,
            'body': submission.selftext,
            'url': submission.url,
            'created_at': submission.created_utc,
            'redditor': {
                'id': submission.author.id,
                'name': submission.author.name
            }}
        print("Sending a new submission")
        print(submission_info)
        producer.send('submissions', json.dumps(
            submission_info).encode('utf8'))


def main():
    args = parse_args()

    print("Start fetching data from Reddit")

    reddit = praw.Reddit(
        client_id="***REMOVED***",
        client_secret="***REMOVED***",
        user_agent="graph-demo data fetcher")

    p1 = Process(target=lambda: produce_submissions(reddit, args.subreddit))
    p1.start()
    p2 = Process(target=lambda: produce_comments(reddit, args.subreddit))
    p2.start()

    p1.join()
    p2.join()


if __name__ == "__main__":
    main()
