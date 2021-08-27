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
            created_object = {
                'id': obj['vertex'].id,
                'labels': [label.name for label in obj['vertex'].labels],
            }
            if obj['vertex'].labels[0].name == "SUBMISSION":
                created_object.update({
                    'sentiment': obj['vertex'].properties['sentiment'],
                    'title': obj['vertex'].properties['title'],
                })
            elif obj['vertex'].labels[0].name == "COMMENT":
                created_object.update({
                    'sentiment': obj['vertex'].properties['sentiment'],
                    'body': obj['vertex'].properties['body'],
                })
            else:
                created_object.update({
                    'name': obj['vertex'].properties['name'],
                })
            created_objects_info['vertices'].append(created_object)
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
