from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import requests 
from datetime import datetime, timedelta


args = {
 
    'owner': 'esperancia_daniel',
    'start_date': days_ago(1)
}

dag = DAG(dag_id = 'project_producer_d04', default_args=args, schedule_interval=timedelta(seconds=5))




url = "http://host.docker.internal:8888/getdata"
topic_name = "data"

def pushData():

    data = getData()
    producer = KafkaProducer(bootstrap_servers=['kafka1:9093'])

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



def getData():
    response = requests.get(url)
    responseJson = response.text
    #print(responseJson)
    return responseJson


def error_callback(exc):
    raise Exception('Error while sendig data to kafka: {0}'.format(str(exc)))


    

with dag:

    produce_task = PythonOperator(
        task_id='produce_task',
        python_callable = pushData
    )


    produce_task