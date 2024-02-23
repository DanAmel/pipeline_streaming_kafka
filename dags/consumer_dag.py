from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
from base64 import b64encode
import requests 
import json


args = {
 
    'owner': 'esperancia_daniel',
    'start_date': days_ago(1)
}

dag = DAG(dag_id = 'project_consumer_d04', default_args=args, schedule_interval=None)



# Encodage des données en Base64
def encode_to_base64(value):
    return b64encode(value.encode()).decode()



baseUrl = "http://host.docker.internal:16201/"
table = "stream_db"


def consumeData():
    consumer = KafkaConsumer("data", group_id="esperancia_daniel", bootstrap_servers=['kafka1:9093'])

    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                            message.offset, message.key,
                                            json.loads(message.value)))
        value = json.loads(message.value)
        #table.put(value["customer"], {'device': value["device"], 'action': value["action"], 'time': value["time"] })
        
        
        headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
        }
        row_key = (value["customer"])
        data = {
                "Row": [
                    {
                        "key": encode_to_base64(row_key),
                        "Cell": [
                            {
                                "column": encode_to_base64("customer:nom"),
                                "$": encode_to_base64(value["customer"])
                            },
                            {
                                "column": encode_to_base64("action:action"),
                                "$": encode_to_base64(value["action"])
                            },
                            {
                                "column": encode_to_base64("time:time"),
                                "$": encode_to_base64(value["time"])
                            },
                            {
                                "column": encode_to_base64("device:device"),
                                "$": encode_to_base64(value["device"])
                            }
                        ]
                    }
                ]
            }
        
        
        print(f"{json.dumps(data)}")
        response = requests.put(f"{baseUrl}{table}/fakerow", headers=headers, data=json.dumps(data))
        responseJson = response.text
        print(responseJson)
        #return responseJson


with dag:

    consume_task = PythonOperator(
        task_id='consume_task',
        python_callable = consumeData
    )


    consume_task