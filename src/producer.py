from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import requests 
import time
import json


url = "http://127.0.0.1:8080/getdata"
topic_name = "data"

def pushData():

    data = getData()
    #print("yoy ", data)
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    # Asynchronous by default
    future = producer.send(topic_name,data.encode("utf-8")).add_errback(error_callback)

    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as e:
        # Decide what to do if produce request failed...
        print(e)
        return None

    # Successful result returns assigned partition and offset
    print (record_metadata.topic)
    print (record_metadata.partition)
    print (record_metadata.offset)



def consumeData():
    consumer = KafkaConsumer(topic_name, group_id="daniel", bootstrap_servers=['127.0.0.1:9092'])
    #KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                            message.offset, message.key,
                                            message.value))

def getData():
    response = requests.get(url)
    responseJson = response.text
    #print(responseJson)
    return responseJson


def error_callback(exc):
    raise Exception('Error while sendig data to kafka: {0}'.format(str(exc)))


#consumeData()

#consumeData()

while True:
    print("sending data...")
    pushData()
    time.sleep(5)