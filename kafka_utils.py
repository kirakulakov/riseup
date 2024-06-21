from kafka import KafkaProducer, KafkaConsumer
import json

KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def get_kafka_consumer(topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def send_message(producer, topic, message):
    producer.send(topic, message)
    producer.flush()

def consume_messages(consumer, callback):
    for message in consumer:
        callback(message.value)