import streamlit as st
from kafka import KafkaConsumer

# Kafka consumer configuration
bootstrap_servers = 'broker:29092'
topic_name = 'processed-data'

# Set up Kafka consumer
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_servers,
)

# Set up Streamlit app
st.title('Network Traffic Analysis Dashboard')

# Read and display the processed data from Kafka topic
for message in consumer:
    window, source_ip, total_bytes_sent = message.value.decode('utf-8').split(',')
    #st.write('Window:', window)
    st.write('Destination IP:', window)
    st.write('Source IP:', source_ip)
    st.write('Total Bytes Sent:', total_bytes_sent)
    st.write('---')  # Add a separator between data points
