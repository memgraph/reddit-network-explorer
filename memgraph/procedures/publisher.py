import mgp
import pickle
from kafka import KafkaProducer


KAFKA_ENDPOINT = 'kafka:9092'


@mgp.read_proc
def create(created_objects: mgp.Any
           ) -> mgp.Record():
    created_objects_info = {'vertices': [], 'edges': []}

    for obj in created_objects:
        if obj['event_type'] == 'created_vertex':
            created_objects_info['vertices'].append({
                'id': obj['vertex'].id,
                'labels': [label.name for label in obj['vertex'].labels]
            })
        else:
            created_objects_info['edges'].append({
                'id': obj['edge'].id,
                'type': obj['edge'].type.name,
                'from': obj['edge'].from_vertex.id,
                'to': obj['edge'].to_vertex.id
            })

    kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_ENDPOINT)
    kafka_producer.send('created_objects', pickle.dumps(created_objects_info))

    return None
