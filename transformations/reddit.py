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
                query="MATCH (p {id: $parent_id}) CREATE (c:COMMENT {id: $id, body: $body}) MERGE (r:REDDITOR {id: $redditor_id, name: $redditor_name}) CREATE (c)-[:CREATED_BY]->(r) CREATE (c)-[:REPLY_TO]->(p)",
                parameters={
                    "parent_id": comment_info["parent_id"],
                    "body": comment_info["body"],
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
        comment_info = pickle.loads(message.payload())
        result_queries.append(
            mgp.Record(
                query="CREATE (s:SUBMISSION {id: $id, title: $title}) MERGE (r:REDDITOR {id: $redditor_id, name: $redditor_name}) CREATE (s)-[:CREATED_BY]->(r)",
                parameters={
                    "title": comment_info["title"],
                    "id": comment_info["id"],
                    "redditor_id": comment_info["redditor"]["id"],
                    "redditor_name": comment_info["redditor"]["name"]}))

    return result_queries
