from argparse import ArgumentParser
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable
from time import sleep
import praw
import pickle
from multiprocessing import Process


KAFKA_ENDPOINT='kafka:9092' 

def parse_args():
    """
    Parse input command line arguments.
    """
    parser = ArgumentParser(
        description="A Reddit subreddit stream machine powered by Memgraph.")
    parser.add_argument("--subreddit", help="Subreddit to be scraped.")
    return parser.parse_args()


def produce_comments(reddit, subreddit):
    producer = KafkaProducer(bootstrap_servers=KAFKA_ENDPOINT)

    for comment in reddit.subreddit(
            subreddit).stream.comments(skip_existing=True):
        comment_info = {
            'id': comment.id,
            'body': comment.body,
            'redditor': {
                'id': comment.author.id,
                'name': comment.author.name
            },
            'parent_id': comment.parent_id[3:]}
        print("Sending a new comment")
        print(comment_info)
        producer.send('comments', pickle.dumps(comment_info))


def produce_submissions(reddit, subreddit):
    producer = KafkaProducer(bootstrap_servers=KAFKA_ENDPOINT)

    for submission in reddit.subreddit(
            subreddit).stream.submissions(skip_existing=False):
        submission_info = {
            'id': submission.id,
            'title': submission.title,
            'redditor': {
                'id': submission.author.id,
                'name': submission.author.name
            }}
        print("Sending a new submission")
        print(submission_info)
        producer.send('submissions', pickle.dumps(submission_info))


def get_admin_client():
    retries = 10
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
            sleep(1)
        
def main():
    args = parse_args()

    admin_client = get_admin_client()

    topic_list = [
        NewTopic(
            name="comments",
            num_partitions=1,
            replication_factor=1),
        NewTopic(
            name="submissions",
            num_partitions=1,
            replication_factor=1)]
    
    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    except TopicAlreadyExistsError:
      pass 

    reddit = praw.Reddit(
        client_id="nDtB4H_xsfNGBckKxYKb3Q",
        client_secret="JqLwl4a3fVBfEPSeICh5M8k-KUxkvg",
        user_agent="graph-demo data fetcher")

    p1 = Process(target=lambda: produce_submissions(reddit, args.subreddit))
    p1.start()
    p2 = Process(target=lambda: produce_comments(reddit, args.subreddit))
    p2.start()

    p1.join()
    p2.join()


if __name__ == "__main__":
    main()
