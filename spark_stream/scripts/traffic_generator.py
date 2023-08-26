from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import time
import random

# Kafka producer configuration
bootstrap_servers = 'broker:29092'
topic_names = ['network-traffic','processed-data']

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
)

# List topics available
admin_client = KafkaAdminClient(bootstrap_servers='broker:29092')

topics = admin_client.list_topics()

# Create network-traffic and processed-data topics if they do not exist
for topic_name in topic_names:
    if topic_name not in topics:
        try:
            admin = KafkaAdminClient(bootstrap_servers='broker:29092')
            topic = NewTopic(name=topic_name,num_partitions=1,replication_factor=1)
            admin.create_topics([topic])
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic_name, e))
print(topics)

# Generate and publish network traffic data to Kafka topic
while True:
    # Generate random network traffic data
    source_ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    destination_ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    bytes_sent = random.randint(1000, 100000)

    # Publish network traffic data to Kafka topic
    producer.send(topic_name, f"{source_ip},{destination_ip},{bytes_sent}".encode('utf-8'))

    # Wait for 1 second before generating the next network traffic data
    time.sleep(1)
