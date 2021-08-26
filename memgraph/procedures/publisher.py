import json
import mgp
import os
from kafka import KafkaProducer


KAFKA_IP = os.getenv('KAFKA_IP', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')


@mgp.read_proc
def create(created_objects: mgp.Any
           ) -> mgp.Record():
    created_objects_info = {'vertices': [], 'edges': []}

    for obj in created_objects:
        if obj['event_type'] == 'created_vertex':
            if obj['vertex'].labels[0].name != "REDDITOR":
                created_objects_info['vertices'].append({
                    'id': obj['vertex'].id,
                    'labels': [label.name for label in obj['vertex'].labels],
                    'sentiment': obj['vertex'].properties['sentiment'],
                })
            else:
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

    kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_IP + ':' + KAFKA_PORT)
    kafka_producer.send('created_objects', json.dumps(
        created_objects_info).encode('utf8'))

    return None
