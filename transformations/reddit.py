import mgp
import pickle


@mgp.transformation
def comments(messages: mgp.Messages
             ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        comment_info = pickle.loads(message.payload())
        result_queries.append(
            mgp.Record(
                query=("MATCH (p {id: $parent_id}) "
                       "CREATE (c:COMMENT {id: $id, body: $body, created_at: $created_at}) "
                       "MERGE (r:REDDITOR {id: $redditor_id, name: $redditor_name}) "
                       "CREATE (c)-[:CREATED_BY]->(r) "
                       "CREATE (c)-[:REPLY_TO]->(p)"),
                parameters={
                    "parent_id": comment_info["parent_id"],
                    "body": comment_info["body"],
                    "created_at": comment_info["created_at"],
                    "id": comment_info["id"],
                    "redditor_id": comment_info["redditor"]["id"],
                    "redditor_name": comment_info["redditor"]["name"]}))

    return result_queries

@mgp.transformation
def submissions(messages: mgp.Messages
             ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        submission_info = pickle.loads(message.payload())
        result_queries.append(
            mgp.Record(
                query=("CREATE (s:SUBMISSION {id: $id, title: $title, body: $body, url: $url, created_at: $created_at}) "
                       "MERGE (r:REDDITOR {id: $redditor_id, name: $redditor_name}) "
                       "CREATE (s)-[:CREATED_BY]->(r)"),
                parameters={
                    "title": submission_info["title"],
                    "body": submission_info["body"],
                    "url": submission_info["url"],
                    "created_at": submission_info["created_at"],
                    "id": submission_info["id"],
                    "redditor_id": submission_info["redditor"]["id"],
                    "redditor_name": submission_info["redditor"]["name"]}))

    return result_queries
